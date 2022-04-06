"""
author: Ziwen Yuan

This script is used to analyze token statistics of raw Python3 programs.

This script is also used to obtain the statistics relative to 
the length of raw JavaScript programs. Other JavaScript programs statisitcs
should be obtained using the javascript_tokenizer.js script.

This script use `tokenize` module to tokenize raw Python3 programs.
This module comes with the Python3 standard library, no extra installation requried.
"""
import argparse
import os
import tokenize

def analyze_py(folder, lang, dataset):
    count = 1
    file_name = folder + lang +'/'+ lang+'_'+dataset+'_'+str(count)+'.'+lang
    file = open(file_name, 'r')
    total_length = 0
    total_tokens = []
    total_token_num = 0

    while True:
        # process one file
        file_length = sum(1 for line in file if line.rstrip())
        file.close()
        file = open(file_name,'r')
        file_tokens = []
        if file_length == 0:
            print('stopped at empty file:', file_name)
            break 
        for i in range(file_length):
            line_tokens_generator = tokenize.generate_tokens(file.readline)
            for token in line_tokens_generator:
                token_string = ''
                if token.string == '':
                    token_string = 'EMPTY_STRING'
                elif token.string.isspace():
                    token_string = token.string.replace('    ','TAB')
                else:
                    token_string = token.string

                if token_string not in file_tokens:
                    file_tokens.append(token_string)

        total_length += file_length
        total_tokens += file_tokens
        file_token_num = len(file_tokens)
        total_token_num += file_token_num  
        count +=1
        file_name = folder + lang +'/'+ lang+'_'+dataset+'_'+str(count)+'.'+lang
        if os.path.exists(file_name):
            file = open(file_name, 'r')
        else:
            print('stopped at not-exist file:', file_name)
            break      
        
    count -= 1
    total_unique_tokens = [tok for tok in set(total_tokens)]
    average_program_length = total_length / count
    average_token_num = total_token_num / count
    print('Total Program Num:', count)
    print('Average Program Length per Program:', average_program_length)
    print('Average Token Num per Program:', average_token_num)
    print('All Unique Token Num across Programs:', len(total_unique_tokens))
    print('FINISHED')

def analyze_js(folder, lang, dataset):
    count = 1
    file_name = folder + lang +'/'+ lang+'_'+dataset+'_'+str(count)+'.'+lang
    file = open(file_name, 'r')
    total_length = 0

    while True:
        # process one file
        file_length = sum(1 for line in file if line.rstrip())
        if file_length == 0:
            print('stopped at empty file:', file_name)
            break    
        file.close()
        total_length += file_length
        count +=1
        file_name = folder + lang +'/'+ lang+'_'+dataset+'_'+str(count)+'.'+lang
        if os.path.exists(file_name):
            file = open(file_name, 'r')
        else:
            print('stopped at not-exist file:', file_name)
            break      
        
    count -= 1
    average_program_length = total_length / count
    average_token_num = 'Please use JavaScript tokenizer to obtain this info'
    total_unique_tokens_num = 'Please use JavaScript tokenizer to obtain this info'
    print('Total Program Num:', count)
    print('Average Program Length per Program:', average_program_length)
    print('Average Token Num per Program:', average_token_num)
    print('All Unique Token Num across Programs:', total_unique_tokens_num)
    print('FINISHED')

parser = argparse.ArgumentParser(description='provide me detail of which parse tree string(s) to be converted into JSON file.')
parser.add_argument('--dataset',choices=['train','valid','atom_test'])

parser.add_argument('--train',action='store_true')
parser.add_argument('--valid',action='store_true')
parser.add_argument('--atom',action='store_true')
parser.add_argument('--py',action='store_true')
parser.add_argument('--js',action='store_true')

args = parser.parse_args()

if args.train:
    folder = 'data/train_data/'
    dataset = 'train'
elif args.valid:
    folder = 'data/validation_data/'
    dataset = 'validation'
elif args.atom:
    folder = 'data/atom_test_data/'
    dataset = 'atom_test'
else:
    print('add option --train or --valid or --atom to indicate which data folder you want to process.')
    os.sys.exit()

if args.py:
    lang = 'py'
    analyze_py(folder, lang, dataset)
elif args.js:
    lang = 'js'
    analyze_js(folder, lang, dataset)
else:
    print('add option --js or --py to indicate which language programs you want to process.')
    os.sys.exit()


