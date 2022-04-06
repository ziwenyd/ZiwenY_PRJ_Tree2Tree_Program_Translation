"""
author: Ziwen Yuan

The Python3 TreeParser built on top of ANTLR4 with selected Python3 grammar
requires input file to have extra blank line at the end of the file, otherwise the generated
parse tree will have miss-leading information.

This script is used to validate all Python3 programs before passing to ANTLR4 TreeParser Java class.

This script ensures all .py file have two blank lines at the end of the file.
For empty .py files, this script also add two blank lines at the end of the file,
This validation process is needed for a success run when using ANTLR4 to parse .py file.
"""
import argparse
import os
def validate():
    folder_under_data = args.folder
    data_type = folder_under_data[:-5]
    count = 1
    root_dir = os.getcwd()
    while True:
        py_file_name = root_dir+'/data/'+folder_under_data+'/py/py_'+data_type+'_'+str(count)+'.py'
        if os.path.exists(py_file_name):
            py_file_read = open(py_file_name, 'r') # read only
            py_file_append = open(py_file_name, 'a') # append text
            lines = py_file_read.readlines()
            if len(lines) == 0: # empty file
                py_file_append.write("\n")
                py_file_append.write("\n")
            elif len(lines) == 1 and lines[0] !="\n":
                py_file_append.write("\n")
                py_file_append.write("\n")
            elif len(lines) == 1 and lines[0] == "\n":
                py_file_append.write("\n")
            elif lines[-1] == "\n" and lines[-2] == "\n":
                pass
            elif lines[-1]=="\n" and lines[-2] != "\n":
                py_file_append.write("\n")
            elif lines[-1] != "\n":
                py_file_append.write("\n")
                py_file_append.write("\n")
            count += 1
        else:
            print('Stopped, because this file does not exist: '+py_file_name)
            break
    print('FINISHED VALIDATION, ALL Python Programs contain 2 blank lines at the end.')


parser = argparse.ArgumentParser(description='provide me detail of which parse tree string(s) to be converted into JSON file.')
parser.add_argument('--folder',default='train_data',
help="The folder under /data/ which contrains raw python program file(default:train_data)")
args = parser.parse_args()

if __name__ == "__main__":
    validate()