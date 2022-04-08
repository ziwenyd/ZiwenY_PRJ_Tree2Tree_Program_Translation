# The parser Folder

This folder contains source code of data processing; typically refer to the Dataset chapter of the report.

Source code in this folder serves the following objectives:

0. Contains dataset
   0.1 dataset are all saved under /parser/data, folder structure is:
   /data/train_data/py
   /data/train_data/js
   /data/train_data/py_ast_str
   /data/train_data/js_ast_str

   /data/validation_data/py
   /data/validation_data/js
   /data/validation_data/py_ast_str
   /data/validation_data/js_ast_str

   /data/atom_test_data/py
   /data/atom_test_data/js
   /data/atom_test_data/py_ast_str
   /data/atom_test_data/js_ast_str
   /data/atom_test_data/write_atom_test_feature.py:store which atom test data represent which features.
   /data/atom_test_data/atom_test_feature.csv: result of the previous file.

   /data/source_py_target_js_train.json
   /data/source_py_target_js_validation.json
   /data/source_py_target_js_atom_test.json

1. Build .json file in the desired format as Tree2Tree input, for training data, validation data, and atom test data.
   1.1 parse_data_atom_test.sh, parse_data_train.sh, parse_data_valid.sh: generate string-formatted parse trees for a the raw data folder recursively. (saved under /parser/data/xx_data/xx_ast_str, postfixed as '\_ast_str.txt').
   1.1.1 python_parser/TreeParser: the parser to obtain Python3 parse tree
   1.1.2 javascript_parser/TreeParser: the parser to obtain JavaScript parse tree
   1.1.3 validate_python.py: check all Python raw programs have 2 black lines at the end
   1.2 build_json_from_parse_tree: build .json file as input of the Tree2Tree model, uses the ast_str.txt files built in 1.1.
2. Dataset Statistics Calculation, which is used in the Evaluation chapter in the report.
   2.1 javascript_tokenizer.js: tokenize raw Javascript program; calcualte statistics; print to the terminal.
   2.2 raw_program_analyzer.py: tokenizer raw Python program; calcualte statistics; print to the terminal.

# Convert Raw Progrms into JSON

## Train

```bash
sh parse_data_train.sh

python3 build_json_from_parse_tree.py
```

## Validation

```bash
sh parse_data_valid.sh

python3 build_json_from_parse_tree.py \
--folder validation_data \
--result_file_name source_py_target_js_validation
```

## Atom Test

```bash
sh parse_data_atom_test.sh

python3 build_json_from_parse_tree.py \
--folder atom_test_data \
--result_file_name source_py_target_js_atom_test
```

---

# ANTLR4

## ANTLR 4 Resources

Book: file:///tmp/mozilla_k18023120/The%20definitive%20ANTLR%204%20reference%20by%20Terence%20Parr%20(z-lib.org).pdf

ANTLR4 GitHub repo: https://github.com/antlr/antlr4/blob/master/doc/getting-started.md

ANTLR4 GitHub repo Python2/3: https://github.com/antlr/antlr4/blob/master/doc/python-target.md

good tutorial: https://tomassetti.me/antlr-mega-tutorial/#chapter37

## Install ANTLR4

Download the jar of ANTLR4(require Java 1.7+)

### Set up the Environment

On KCL Informtics Lab Machine (Linux):

```bash
export CLASSPATH=".:/home/k1802312/Desktop/parser/antlr-4.9-complete.jar:$CLASSPATH"

alias antlr4='java -Xmx500M -cp "/home/k1802312/Desktop/parser/antlr-4.9-complete.jar:$CLASSPATH" org.antlr.v4.Tool'

alias grun='java -Xmx500M -cp "/home/k1802312/Desktop/parser/antlr-4.9-complete.jar:$CLASSPATH" org.antlr.v4.gui.TestRig'

java org.antlr.v4.Tool
antlr4
```

On my own macbook (MacOS):

```bash
export CLASSPATH=".:/Users/yuanziwen/Desktop/parser/antlr-4.9-complete.jar:$CLASSPATH"

alias antlr4='java -Xmx500M -cp "/Users/yuanziwen/Desktop/parser/antlr-4.9-complete.jar:$CLASSPATH" org.antlr.v4.Tool'

alias grun='java -Xmx500M -cp "/Users/yuanziwen/Desktop/parser/antlr-4.9-complete.jar:$CLASSPATH" org.antlr.v4.gui.TestRig'

java org.antlr.v4.Tool
antlr4
```

## Grammar, TreeParser

language specific instruction:
Python3: check the README in the python_parser folder.
JavaScript: check the README in the javascript_parser folder.

## Parse a Progrm File

### Python3

```bash
cd python_parser
javac *.java   #compile all the Java Code
java ParseTree <py_file_to_generate_parse_tree>
```

### JavaScript

```bash
cd javascript_parser
javac *.java  #compile all the Java Code
java ParseTree <js_file_to_generate_parse_tree>
```

## Generate a GUI Parse Tree

Replace -gui as -tokens, to generate tokens of programs in real time.

### Python3

```bash
cd python_parser
grun Python3 single_input -gui
```

Python3 is the grammar name.

### JavaScript

```bash
cd javascript_parser
grun JavaScript program -gui
```

JavaScript is the grammar name.

## Use the ANTLR parsers to obtain all parse trees

```bash
sh parse_data.sh
```

## Generate Input JSON file

```bash
python3 build_tree_dict.py
```
