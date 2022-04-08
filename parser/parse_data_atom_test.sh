# author: Ziwen Yuan

# This shell script is used to perform the workflow on atom test dataset.
# The workflow includes:
# - validate Python raw data
# - use TreeParser to generate string-formatted parse tree of Python dataset.
# - use TreeParser to generate string-formatted parse tree of JavaScript dataset.

# The raw Python and JavaScript datasets are saved in the following directories:
# - /parser/data/atom_test_data/js
# - /parser/data/atom_test_data/py

# The generated string-formatted parse tree are placed in the following folder with '_ast_str.txt' postfix.
# - /parser/data/atom_test_data/js_ast_str
# - /parser/data/atom_test_data/py_ast_str
###############

python3 validate_python.py --folder atom_test_data
cd python_parser
javac *.java
for i in ../data/atom_test_data/py/*.py; do java TreeParser "$i"; done
cd ..
cd javascript_parser
javac *.java
for i in ../data/atom_test_data/js/*.js; do java TreeParser "$i"; done
echo "parsed all data/atom_test_data data, saved the parse tree(string format) in the same folder"