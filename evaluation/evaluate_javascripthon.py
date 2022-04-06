"""
author: Ziwen Yuan
Evaluate the translation result obtained using JavaScripthon.

Evaluation Metrics included in this script: 
- Token Accuracy
- Program Accuracy
- Edit Token Distance Ratio (EDR)
"""
import os

# token accuracy and program accuray for one (output, target) pair data


def token_and_program_accuracy(output, target):
    """
    Calculate the token accuracy and program accuracy of 
    one data sample, i.e one (translation output, ground-truth target) pair.
    @param output: list of tokens
    @param target: list of tokens
    """
    total_token_num = len(target)
    correct_token_num = 0
    program_accuracy = 1 if len(output) > 0 else 0
    wrong_and_desired_tokens = []  # [(wrongly_predicted_token, desired_token)]
    for i in range(len(output)):
        if i >= len(target):
            break
        if output[i] == target[i]:
            correct_token_num += 1
        else:
            program_accuracy = 0
            wrong_and_desired_tokens.append([output[i], target[i]])
    return correct_token_num, total_token_num, program_accuracy

# edit distance for one (output, target) pair data


def edit_distance(output, target):
    """
    Calculate the edit distance of 
    one data sample, i.e. one (translation output, ground-truth target) pair.
    @param output: list of tokens
    @param target: list of tokens
    """
    output_len = len(output)
    target_len = len(target)
    OPT = [[0 for i in range(target_len+1)]
           for j in range(output_len + 1)]  # DP table

    # OPT[i][0] = i, assign values to first column
    for i in range(1, output_len+1):
        OPT[i][0] = i
    # OPT[0][j] = j, assign values to first row
    for j in range(1, target_len+1):
        OPT[0][j] = j

    single_insert_cost = 1
    single_delete_cost = 1
    single_align_cost = 1
    for i in range(1, output_len+1):  # row
        for j in range(1, target_len+1):  # column
            delta = single_align_cost if output[i-1] != target[j-1] else 0
            alignment_cost = OPT[i-1][j-1] + delta
            delete_cost = OPT[i-1][j] + single_delete_cost
            insertion_cost = OPT[i][j-1] + single_insert_cost
            OPT[i][j] = min(alignment_cost, delete_cost, insertion_cost)
    return OPT[output_len][target_len], output_len

# process '_tokenized.txt' files to save tokens into a list


def process_data():
    output_folder = 'javascripthon_atom_test_result/'
    target_folder = '../parser/data/atom_test_data/js_tokenized/'
    dataset = 'atom_test'
    output_lang_in_file_name = 'py'
    target_lang_in_file_name = 'js'
    count = 1
    output_file_name = output_folder + output_lang_in_file_name + \
        '_'+dataset+'_'+str(count)+'_tokenized.txt'
    target_file_name = target_folder + target_lang_in_file_name + \
        '_'+dataset+'_'+str(count)+'_tokenized.txt'
    output_file = open(output_file_name, 'r')
    target_file = open(target_file_name, 'r')
    outputs = []
    targets = []
    while True:
        output = output_file.read().split()
        target = target_file.read().split()
        outputs.append(output)
        targets.append(target)

        count += 1
        output_file_name = output_folder + output_lang_in_file_name + \
            '_'+dataset+'_'+str(count)+'_tokenized.txt'
        target_file_name = target_folder + target_lang_in_file_name + \
            '_'+dataset+'_'+str(count)+'_tokenized.txt'
        if os.path.exists(output_file_name) and os.path.exists(target_file_name):
            output_file = open(output_file_name, 'r')
            target_file = open(target_file_name, 'r')
        else:
            print('stopped at not-exist file:', output_file_name)
            break
    return outputs, targets

# perform evaluation on the whole dataset and print result in the terminal.


def evaluate(outputs, targets):
    """
    Perform evaluation, give scores of selected evaluation metrics.
    @param output: a list of list of tokens. each nested list represents one data sample.
    @param target: a list of list of tokens. each nested list represents one data sample.
    """
    if len(outputs) != len(targets):
        print('translation result data size differs from ground thuth data size. Something WRONG.')
        print('Terminated.')
        os.sys.exit()
    EDR = 0
    total_edit_distance = 0
    TokenAccuracy = 0
    ProgramAccuracy = 0
    total_output_token_num = 0
    total_target_token_num = 0
    correct_token_num = 0
    correct_program_num = 0
    total_program_num = len(outputs)

    for i in range(len(outputs)):
        output = outputs[i]
        target = targets[i]
        # token accuracy and program accuracy
        one_correct_token_num, one_target_token_num, one_correct_program_num = token_and_program_accuracy(
            output, target)
        total_target_token_num += one_target_token_num
        correct_token_num += one_correct_token_num
        correct_program_num += one_correct_program_num
        # EDR
        one_edit_distance, one_output_token_num = edit_distance(output, target)
        total_output_token_num += one_output_token_num
        total_edit_distance += one_edit_distance

    TokenAccuracy = correct_token_num / total_target_token_num
    ProgramAccuracy = correct_program_num / total_program_num
    EDR = total_edit_distance / total_output_token_num
    print('total Program Num,', len(outputs))
    print('total correct token num', correct_token_num,
          'total target token num', total_target_token_num, 'total output token num', total_output_token_num)
    print('token accuracy:', TokenAccuracy)
    print('program accuracy:', ProgramAccuracy)
    print('Token Edit Distance Ratio(EDR):', EDR)


if __name__ == '__main__':
    outputs, targets = process_data()
    evaluate(outputs, targets)
