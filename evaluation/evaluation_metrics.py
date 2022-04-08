"""
author: Ziwen Yuan

This file calculates the 
 - Atom Feature Accuracy,
 - Compile Accuracy(because JavaScript is an interpreter language, this is the same as run-ability),
 - Computational Accuray
for the translation result of JavaScripthon,
on the atom test dataset created in this project.
However, this script can be easily extended to calculate
atom feature accuracy for any other projects.

For the theory part of Atom Feature Accuracy,
including the inspiration and calculation equation,
please check the `Evaluation Metrics` chapter in the report.

Before running this script, you should run the 
get_execution_result.sh
shell script in the same folder, to obtain the execution result
of output and target data, saved into corresponding .txt files
under the same folder:
- the_output_execution.txt
- the_target_execution.txt
"""
from distutils.log import error
from importlib.abc import TraversableResources
import os
import csv

def compile_accuracy(outputs):
    error_num = 0
    for i in range(len(outputs)):
        if "<ERROR>" == outputs[i][0]:
            error_num +=1
    compile_accuracy = (len(outputs)-error_num)/len(outputs)
    print("Compile Accuracy = "+str(compile_accuracy))

def computational_accuracy(outputs, targets,output_files_order, target_files_order):
    unmatch_outputs = []
    unmatch_targets = []
    unmatch_file_counts = []
    matched_num = 0
    for i in range(len(outputs)):
        output = outputs[i]
        target = targets[i]
        match = True
        for j in range(len(output)): #each line of execution result
            if j >= len(target):
                match = False
                break
            if output[j] != target[j]:
                match = False
                break
            # if output[j] == target[j], 
            # continue to the next output[j]

        if not match:
            unmatch_file_counts.append(target_files_order[i])
            unmatch_outputs.append(outputs[i])
            unmatch_targets.append(targets[i])
        else:
            matched_num +=1
    print("Program number = "+str(len(outputs)))
    print("Computational Accuracy = "+str( matched_num/len(outputs)) )
    return unmatch_outputs, unmatch_targets, unmatch_file_counts

def atom_feature_accuracy(atom_feature_scores_dir, outputs, targets, output_files_order, target_files_order, feature_map):
    """
    Calculate Atom Feature Accuracy.
    Feature map is needed, this can be written in one csv file and use 
    the get_feature_map() function to extract data into the desired format`feature map`.
    """
    f = open(atom_feature_scores_dir, 'w', encoding='UTF8')
    header = ['feature','atom feature accuracy','output execution results','target execution results']
    csv_writer = csv.writer(f)
    csv_writer.writerow(header)
    file_count_to_idx = {}
    for idx in range(len(output_files_order)):
        file_count = output_files_order[idx]
        file_count_to_idx[file_count] = idx
    
    # calculate feature accuracy for each feature
    feature_accuracies = []
    sum_feature_accuracy = 0
    for i in range(len(feature_map)):
        single_feature_match_num = 0
        feature = feature_map[i][0]
        feature_accuracies.append([feature,0,[],[]])
        feature_file_counts = feature_map[i][1]
        feature_output_file_counts = []
        feature_target_file_counts = []
        for file_count in feature_file_counts:
            idx = file_count_to_idx[file_count]
            output = outputs[idx]
            target = targets[idx]
            feature_output_file_counts.append(output)
            feature_target_file_counts.append(target)
            if output == target:
                single_feature_match_num += 1
        single_feature_accuracy = single_feature_match_num / len(feature_file_counts)
        sum_feature_accuracy += single_feature_accuracy
        feature_accuracies[i][1] = single_feature_accuracy
        feature_accuracies[i][2] = feature_output_file_counts
        feature_accuracies[i][3] = feature_target_file_counts

    csv_writer.writerows(feature_accuracies)

    feature_num = len(feature_accuracies)
    atom_feature_accuracy = sum_feature_accuracy/feature_num
    print("Total Feature Num =", feature_num)
    print("Atom Feature Accuracy =", atom_feature_accuracy)
    print("Feature Accuracies saved in: ", atom_feature_scores_dir)


def get_feature_map(feature_csv_dir):
    """
    return a list of lists.
    each nested list represents one feature
    first item: feature name
    second item: a list of file numbers testing that feature
    """
    f = open(feature_csv_dir, 'r')
    reader = csv.DictReader(f)
    result = []
    for row in reader:
        feature = row['feature']
        file_numbers = row['file_numbers'].split()
        result.append([feature, file_numbers])
    return result

def process_data(output_dir, target_dir):
    """
    Process output and target datasets into two `a list of list`.
    each nested list represents one data sample.
    
    Check the data size of both datasets matches.
    Check the data order of both datasets matches.
    """
    output_files_order, output_errors, output_error_file_counts, outputs = process_one_dataset(output_dir)
    target_files_order, target_errors, target_error_file_counts, targets = process_one_dataset(target_dir)

    # check the outputs and targets size matched
    if len(outputs) != len(targets):
        print('Data Sample numbers differ. Please check your dataset.')
        print('Output dataset size:', len(outputs))
        print('Target dataset size:', len(targets))
        os.sys.exit()

    # check the file order of output and target matched.
    order_match = True
    for i in range(len(output_files_order)):
        if output_files_order[i] != target_files_order[i]:
            print('File does not match: output='+str(output_files_order[i])+
            ';target='+str(target_files_order[i]))
    if not order_match:
        os.sys.exit()

    # check data size matched
    if len(output_error_file_counts) != len(output_errors):
        print('Something Wrong, Unmatched Size, Please check the code.')
        print("output_error_file_counts",output_error_file_counts)
        print("output_errors", output_errors)
        os.sys.exit()

     # check data size matched
    if len(target_error_file_counts) != len(target_errors):
        print('Something Wrong, Unmatched Size, Please check the code.')
        print("target_error_file_counts",target_error_file_counts)
        print("target_errors", target_errors)
        os.sys.exit()

    return output_errors, target_errors, outputs, targets, output_files_order, target_files_order, output_error_file_counts, target_error_file_counts

def process_one_dataset(dir):    
    """
    Process the data into a list of list.
    each nested list represents one data sample.
    """
    file = open(dir, 'r')
    lines = [line[:-1] for line in file.readlines()]# each line has a \n at the end
    results = []
    # record the file number of one data sample saved in `results`.
    # file_number_order and results share the same index.
    file_number_order = [] 
    errors = []
    error_file_counts = []

    count = 0 # file number, this is included in file names.
    one_file_output = []
    for i in range(len(lines)):
        line = lines[i]
        if line.startswith('<FILE>'):
            count = line.replace('<FILE>',"").replace('\n',"")
            if i != 0 :
                results.append(one_file_output)
            file_number_order.append(count)
            one_file_output = []
            continue
        if "Error" in line: # an error message
            errors.append(line.replace('\n',""))
            one_file_output.append("<ERROR>")
            error_file_counts.append(count)
            continue
        one_file_output.append(line)

    results.append(one_file_output)
    
    return file_number_order, errors, error_file_counts, results

def unmatch_analysis(result_dir, output_errors, target_errors,unmatch_outputs,unmatch_targets,unmatch_file_counts,output_error_file_counts,target_error_file_counts):
    f = open(result_dir, 'w', encoding='UTF8')
    header = ['unmached output', 'unmatched target',"file number","",
              'output error', 'occurrence', 'file number(s)', "",'target execution error', 'occurrence', 'file number(s)']
    csv_writer = csv.writer(f)
    csv_writer.writerow(header)
    # intialize what to write in the csv
    csv_result = [["" for i in range(len(header))] for i in range(max(len(output_errors), len(unmatch_outputs)))]
    
    if not (len(unmatch_outputs) == len(unmatch_targets) == len(unmatch_file_counts)):
        print("Data Sample Numbers are NOT the same. Please check the code.")
        print("unmatch_outputs:", len(unmatch_outputs))
        print("unmatch_targets:", len(unmatch_targets))
        print("unmatch_file_counts:", len(unmatch_file_counts))
        os.sys.exit()

    for i in range(len(csv_result)):
        if i >= len(unmatch_outputs):
            break
        unmatch_output = unmatch_outputs[i]
        unmatch_target = unmatch_targets[i]
        file_number = unmatch_file_counts[i]
        csv_result[i][0] = unmatch_output
        csv_result[i][1] = unmatch_target
        csv_result[i][2] = file_number

    #key:error message; value:[occurence, file numbers]
    output_error_message_collection = _get_error_message_collection(output_errors,output_error_file_counts,len(csv_result))
    i = 0
    for key in output_error_message_collection:
        error_message = key
        occurence = output_error_message_collection[key][0]
        files = output_error_message_collection[key][1]
        csv_result[i][4]=error_message
        csv_result[i][5]=occurence
        csv_result[i][6]=" ".join(files)
        i += 1
    
    if len(target_errors) == 0:
        csv_result[0][8]="Ground Truth Target Dataset all run successfully without error message."
    else: # do same thing as did for output_error_message_collection
        target_error_message_collection = _get_error_message_collection(output_errors,output_error_file_counts,len(csv_result))
        i = 0
        for key in target_error_message_collection:
            error_message = key
            occurence = target_error_message_collection[key][0]
            files = target_error_message_collection[key][1]
            csv_result[i][8]=error_message
            csv_result[i][9]=occurence
            csv_result[i][10]=" ".join(files)
            i += 1
    
    csv_writer.writerows(csv_result)
    print("Unmatched Output analysis & Error message anaysis are saved in:", result_dir)

def _get_error_message_collection(errors, error_file_counts, max_length):
    """ 
    This function is used by the unmatch_analysis() function.
    @return error_message_collection = {} #key:error message; value:(occurence, file numbers)
    """
    error_message_collection = {} #key:error message; value:[occurence, file numbers]
    for i in range(max_length):
        if i >= len(errors):
            break
        output_error = errors[i]
        file_number = error_file_counts[i]
        if output_error not in error_message_collection:
            error_message_collection[output_error] = [1, [file_number]]
        else:
            error_message_collection[output_error][0] += 1
            error_message_collection[output_error][1].append(file_number)
    return error_message_collection

def main():
    output_dir = 'the_output_execution.txt'
    target_dir = 'the_target_execution.txt'
    analysis_dir = 'atom_feature_analysis.csv'
    feature_dir = '../parser/data/atom_test_data/atom_test_feature.csv'
    atom_feature_scores_dir = 'atom_feature_distribution.csv'
    # process data
    output_errors, target_errors, outputs, targets, output_files_order, \
    target_files_order, output_error_file_counts, target_error_file_counts  = process_data(output_dir, target_dir)
    # calculate compile accuracy
    compile_accuracy(outputs)
    print('---------')

    # calcualte computational accuracy
    unmatch_outputs, unmatch_targets, unmatch_file_counts = \
        computational_accuracy(outputs, targets,output_files_order, target_files_order)
    print('---------')

    # calculate atom feature accuracy
    feature_map = get_feature_map(feature_dir)
    atom_feature_accuracy(atom_feature_scores_dir, outputs, targets, output_files_order, target_files_order, feature_map)
    print('---------')

    # perform analysis and save result in result_dir
    unmatch_analysis(analysis_dir, output_errors, target_errors, unmatch_outputs, unmatch_targets,\
         unmatch_file_counts,output_error_file_counts,target_error_file_counts)

    

main()




