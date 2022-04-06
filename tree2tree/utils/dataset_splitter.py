"""
This script containts several data splitter functions that 
can be used to split the CS-JS data provided by Chen et al.

Because their original dataset is too large(10+GB) to process.

Data is splitted at JSON object level. 
No JSON obejct will be splitted in the middle.

Code in this script is not very well-written, as it was only used
with real-time experiment on the CS-JS dataset at the beginning 
of my project, it is kept just for reference purpose.
"""
import pdb
import json


def split_pre_progs_BL_train(dataset):
    # training data
    if dataset == 'train':
        f = open("../data/CS-JS/BL/preprocessed_progs_train.json", 'r')
    elif dataset == 'valid':
        # validation data
        f = open("../data/CS-JS/BL/preprocessed_progs_valid.json", 'r')
    elif dataset == 'test':
        # test data
        f = open("../data/CS-JS/BL/preprocessed_progs_test.json", 'r')
    print('loading data....')
    data = json.load(f)  # parse the file, returned a list of python dictionary
    print('data loaded, total json objects num:', len(data))  # result is 100000
    # take the first 1% out of it.
    count = 0
    result_data = []
    print('extracting small json objects.....')
    while count < len(data) * 0.001:
        result_data.append(data[count])
        count += 1
    print('writing into a new file......, obj num:', len(result_data))
    # mini_data holds 100 JSON objects.
    if dataset == 'train':
        with open('../mini_data/CS-JS/BL/preprocessed_progs_train.json', 'w') as json_file:
            json.dump(result_data, json_file)
    elif dataset == 'valid':
        with open('../mini_data/CS-JS/BL/preprocessed_progs_valid.json', 'w') as json_file:
            json.dump(result_data, json_file)
    elif dataset == 'test':
        with open('../mini_data/CS-JS/BL/preprocessed_progs_test.json', 'w') as json_file:
            json.dump(result_data, json_file)
    print('count:', count)
    print('done')


def get_first_object_in_preproessed_progs_train():
    f = open("../mini_data/CS-JS/BL/preprocessed_progs_test.json", 'r')
    print('loading data')
    data = json.load(f)  # parse the file, returned a list of python dictionary
    print('data loaded')
    print('total json objects num:', len(data))  # should be 10
    result_data = [data[0]]  # only want the first object
    print('writing into a new file......')
    with open('../one_object_data/CS-JS/BL/preprocessed_progs_test.json', 'w') as json_file:
        json.dump(result_data, json_file)
    print('done')


def get_raw_js_data():
    f = open("../data/CS-JS/BL/progs_train.json", 'r')
    print('loading data')
    data = json.load(f)  # parse the file, returned a dictionary
    raw_js_list = []
    count = 0
    max = 25

    for one_dict in data:
        if count == max:
            break
        raw_js_list.append(one_dict['raw_js'])
        # raw_js_list.append(one_dict['raw_cs'])
        count += 1

    for idx in range(len(raw_js_list)):
        w_f = 'raw_data/js_train'+str(idx)+'_.js'
        # w_f = 'raw_data/py_train_'+str(idx)+'_.py'
        w_f = open(w_f, 'w')
        w_f.write(raw_js_list[idx][36:])
        w_f.close()
    print('finished!')


split_pre_progs_BL_train('train')
split_pre_progs_BL_train('valid')
split_pre_progs_BL_train('test')
# get_first_object_in_preproessed_progs_train()
# get_raw_js_data()
