"""
author: Ziwen Yuan
A utility script to generate empty files
- save some time when manually creating parallel dataset.
"""
import os
import sys


def generate_empty_files(type, language, start_inclusive, end_inclusive, skip_list=[]):
    """
    type : test, train, vaidation, or atom_test
    start_inclusive: the file num to start generating
    end_inclusive: the file num to finish generating
    language: "py" or "js"
    skip_list: the files to skip generation.
    """
    count = start_inclusive
    while count <= end_inclusive:
        if count in skip_list:
            continue
        else:
            file_dir = os.path.join(
                'data/'+type + '_data/'+language+'/'+language+'_'+type+'_'+str(count)+'.'+language)
            generate_one_file(file_dir)
        count += 1
    print('FINISHED')


def generate_one_file(file_dir):
    if os.path.exists(file_dir):
        sys.exit('WARNNING: File already exists! : '+file_dir)
    else:
        f = open(file_dir, 'w')
        f.close()


TEST = 'test'
ATOM_TEST = 'atom_test'
TRAIN = 'train'
VALIDATION = 'validation'
PYTHON = 'py'
JAVASCRIPT = 'js'

if __name__ == '__main__':
    generate_empty_files(ATOM_TEST, JAVASCRIPT, 36, 40)
    generate_empty_files(ATOM_TEST, PYTHON, 36, 40)
    # generate_empty_files(TRAIN, PYTHON, 1, 25)
    # generate_empty_files(TEST, PYTHON, 1, 25)
    # generate_empty_files(VALIDATION, PYTHON, 1, 25)
    # generate_empty_files(TEST, JAVASCRIPT,1, 25)
    # generate_empty_files(VALIDATION, JAVASCRIPT, 1,25)
