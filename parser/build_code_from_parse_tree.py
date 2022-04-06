"""
author: Ziwen Yuan
This script is not used in the project.
Because the Tree2Tree system uses different 
parse tree serialization algorithm to ANTLR4.

An experimental script to convert 
ANTLR4 generated string-formatted parse tree 
back to raw JavaScript programs (do not support Python).

This script is kept only for future reference.
"""
import build_json_from_parse_tree as json_builder

def convert_tree_to_js_code(parse_tree_json):
    result_tokens = []
    stack = []
    stack.append(parse_tree_json)
    current_root_json = None
    while len(stack) > 0:
        current_root_json = stack.pop()
        current_root_children = current_root_json['children']
        if len(current_root_children)==0: #reach leaf node
            token = current_root_json['root']
            if token == '<EOF>' or token == 'eos':
                result_tokens.append('\n')
                continue
            result_tokens.append(token)
            continue
        current_root_children.reverse()
        stack += current_root_children
    return result_tokens

def write_into_program_file(raw_code_tokens, source_file_name):
    dir = 'test_to_raw_program'
    if 'py' in source_file_name:
        dir +=".py"
    if 'js' in source_file_name:
        dir +='.js'
    f = open(dir, 'w')
    lines = []
    line = ""
    for token in raw_code_tokens:
        if token == '\n' or token == '\\n':
            lines.append(line)
            line = ""
            continue
        if token == '\t' or token == '\\t':
            line += "    "
            continue
        if token == '\t\t' or token =='\\t\\t':
            line += "        "
            continue
        line += token + " "
    lines.append(line)
    f.write("\n".join(lines))
    f.close()
    print('file wrote:', dir)

def program_test():
    file_name = '/Users/yuanziwen/Desktop/tree2tree/result/best_eval_loss_model/js_atom_test_0.txt'
    f = open(file_name,'r')
    parse_tree = f.read()
    parse_tree_token_list = json_builder.get_token_list(parse_tree, file_name)
    parse_tree_json = json_builder.build_dict_ast(parse_tree_token_list)
    if 'js' in file_name:
        raw_code = convert_tree_to_js_code(parse_tree_json)
    if 'py' in file_name:
        print('Sorry, this script does not support converting Python.')
    write_into_program_file(raw_code,file_name)

program_test()