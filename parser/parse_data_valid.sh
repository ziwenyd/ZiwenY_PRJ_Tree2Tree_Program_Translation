# author: Ziwen Yuan

# This shell script is used to perform the workflow on validation dataset.
# The workflow includes:
# - validate Python raw data
# - use TreeParser to generate string-formatted parse tree of Python dataset.
# - use TreeParser to generate string-formatted parse tree of JavaScript dataset.

# The raw Python and JavaScript datasets are saved in the following directories:
# - /parser/data/validation_data/js
# - /parser/data/validation_data/py

# The generated string-formatted parse tree are placed in the following folder with '_ast_str.txt' postfix.
# - /parser/data/validation_data/js_ast_str
# - /parser/data/validation_data/py_ast_str
###############

python3 validate_python.py --folder validation_data
cd python_parser
javac *.java
for i in ../data/validation_data/py/*.py; do java TreeParser "$i"; done
cd ..
cd javascript_parser
javac *.java
for i in ../data/validation_data/js/*.js; do java TreeParser "$i"; done
echo "parsed all validation data, saved the parse tree(string format) in the same foler"