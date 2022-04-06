"""
author: Ziwen Yuan

This script is used to convert string-formatted parse trees into JSON objects.

This script can convert folders of parallel parse trees into one .json file, 
which can then be fed into the Tree2Tree model as input corpus directly.

One can also use this script to convert one single file 
or a specific ast string for test purpose.

Commands to generate `train`, `validation`, `atom test` input for Tree2Tree model
are available in README.md to copy paste straight-away.
"""
import os
import json
import argparse
import pdb

def build_dict_ast(token_list):
    stack = []
    for i in range(len(token_list)):
        token = token_list[i]
        if token == '(':
            stack.append(token)
        elif token == ')':
            inside_parenthese = []
            cur = stack.pop() # the -1 element
            
            while cur != '(':
                inside_parenthese.append(cur)
                cur = stack.pop()
            # Special Case where '(' and ')' are the token themselves.
            if len(inside_parenthese) == 0 :
                """
                create dict with root as '(' or ')' and no children
                For example: (arguments ( ))
                    argument
                      / \
                     (   )
                """
                left_b_dict = {'root':'(', 'children':[]}
                stack.append(left_b_dict)
                right_b_dict = {'root':')', 'children':[]}
                stack.append(right_b_dict)
                continue # continue to the next token
            # reverse the list
            # because appended from right(children) to left(root)
            inside_parenthese.reverse()
            # items inside () except the first one
            # are children of the token right after '('
            root = inside_parenthese.pop(0) 

            # Special Case where '(' and ')' are the token themselves.
            if isinstance(root, dict):
                """ For example (parameters ( typedargslist ))
                         parameters
                     /      |      \
                   (  typedargslist   )
                """
                right_b_dict = {'root':')', 'children':[]}
                left_b_dict = {'root':'(', 'children':[]}
                #append back to the stack, no composed dict is created.
                stack.append(left_b_dict)
                stack.append(root)
                stack = stack + inside_parenthese
                stack.append(right_b_dict)
                continue # continue to the next token
            
            children = inside_parenthese # may be empty or many children
            root_dict = {'root': root, 'children':[]}
            for child in children:
                if isinstance(child, dict):
                    root_dict['children'].append(child)
                elif isinstance(child, str):
                    child_dict = {'root':child, 'children':[]}
                    root_dict['children'].append(child_dict)
            stack.append(root_dict)
        else: # normal token string
            stack.append(token)
    ast_dict = stack[0]
    # remove the right children of the root node
    ast_dict['children'] = ast_dict['children'][:-1]
    return ast_dict

def get_token_list(ast_string, file_name):
    if 'py' in file_name:
        ast_string = ast_string.replace('\\n', '<EOF>')
        #12 whitespaces ' . ........ '
        ast_string = ast_string.replace('            ',' \\n \\t\\t ')
        #8 whitespaces ' . .... '
        ast_string = ast_string.replace('        ',' \\n \\t ')
        #2 whitespaces ' . )'
        ast_string = ast_string.replace('  )', ' eos )')
    ast_string = ast_string.replace('(',' ( ')
    ast_string = ast_string.replace(')',' ) ')
    token_list = ast_string.split()
    return token_list

def write_one_json():
    file_name = args.example_file
    file = open(file_name, 'r')
    file_str = file.read()
    token_list = get_token_list(file_str, file_name)
    dict_ast = build_dict_ast(token_list)
    result_file_dir = file_name[:-3]+'json'
    result_file = open(result_file_dir, 'w')
    result_file.write(json.dumps(dict_ast))
    result_file.close()
    print('Example JSON file is written.')


def prepare_data():
    folder_under_data = args.folder
    data_type = folder_under_data[:-5]
    count = 1
    root_dir = os.getcwd()
    py_file_name = root_dir+'/data/'+folder_under_data+'/py_ast_str/py_'+data_type+'_'+str(count)+'_ast_str.txt'
    js_file_name = root_dir+'/data/'+folder_under_data+'/js_ast_str/js_'+data_type+'_'+str(count)+'_ast_str.txt'
    py_file = open(py_file_name, 'r')
    js_file = open(js_file_name, 'r')
    result = []
    while True:
        # Only fill in target_ast and source_ast, ignore source_prog and target_prog
        one_data = {"source_prog":None, "target_prog":None, 
                    "source_ast":None, "target_ast":None}
        py_str = py_file.read()
        js_str = js_file.read()
        
        py_token_list = get_token_list(py_str, py_file_name)
        py_dict = build_dict_ast(py_token_list)
  
        js_token_list = get_token_list(js_str, js_file_name)
        js_dict = build_dict_ast(js_token_list)
        if len(py_token_list)<=4 or len(js_token_list)<=4:
            #ignore empty program files, 
            # which generates parse tree like '(single_input \\n)', corresponding to 4 tokens
            break
        if args.source == 'py':
            one_data["source_ast"] = py_dict
            one_data["target_ast"] = js_dict
            target_langauge = 'js'
        else:
            one_data["source_ast"] = js_dict
            one_data["target_ast"] = py_dict
            target_langauge = 'py'
        result.append(one_data)
        print('Generated json obj num:', count)
        count +=1
        py_file_name = root_dir+'/data/'+folder_under_data+'/py_ast_str/py_'+data_type+'_'+str(count)+'_ast_str.txt'
        js_file_name = root_dir+'/data/'+folder_under_data+'/js_ast_str/js_'+data_type+'_'+str(count)+'_ast_str.txt'
        
        if os.path.exists(py_file_name) and os.path.exists(js_file_name):
            py_file = open(py_file_name, 'r')
            js_file = open(js_file_name, 'r')
        else:
            print('stopped at not-exist file:', py_file_name)
            break
        
    #write into one big json file
    if args.result_file_name is None:
        result_file_name = 'source_'+args.source+'_target_'+target_langauge+folder_under_data
    else:
        result_file_name = args.result_file_name
    result_file_name = root_dir +'/data/'+result_file_name+'.json'
    result_file = open(result_file_name, 'w')
    result_file.write(json.dumps(result))
    print(len(result))
    print('FINISHED')

      
parser = argparse.ArgumentParser(description='provide me detail of which parse tree string(s) to be converted into JSON file.')
parser.add_argument('--folder',default='train_data',
help="The folder under /data/ which contrains string-formated parse tree .txt files, generated from raw programs using ANTLR4.(default:train_data)")
parser.add_argument('--result_file_name', default='source_py_target_js_train',
help="The name of the resulted json file which will then be used as input data of the Tree2Tree model. Do NOT add the .json postfix. The file will be placed under the root directory.")
parser.add_argument('--source', default='py',choices=['py','js'],
help="The source language")
# store_true saves as 'False'
parser.add_argument('--example', action='store_true',
help="Whether use this program to generate input JSON file for the Tree2Tree model (default False), or use this program to generate a JSON file for one example string-formatted parse tree .txt file (manual set this param to be True.)")
parser.add_argument('--example_file', default='example_js_ast_str.txt',
help="Build JSON file for one example string-formatted parse tree .txt file. (default is 'example_js_ast_str.txt')")
args = parser.parse_args()

def program_test():
    """
    Use this function to test this script.
    """
    #Test the program using customized ast string or file name.
    py_file_name = 'data/atom_test_data/py_ast_str/py_atom_test_'+'1'+'_ast_str.txt'
    py_file = open(py_file_name, 'r')
    ast = py_file.read()
    # ast = "(iterationStatement for ( (variableDeclarationList varModifier variableDeclaration) ; (expressionSequence (singleExpression singleExpression < (singleExpression nums . length))) ; (expressionSequence (singleExpression i ++)) ) )"
    # print("ast str:", ast)
    ast_token = get_token_list(ast, py_file_name)
    print("ast token", ast_token)
    ast_dict = build_dict_ast(ast_token)
    print("ast dict", ast_dict)

if __name__ == '__main__':
    # test()
    # program_test()
    if args.example:
        write_one_json()
    else:
        prepare_data()
    
