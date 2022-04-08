# The Evaluation Folder

This evaluation folder contains source code used during evaluation process.
Typically refers to the Evaluation chapter in the PRJ report.

Source code in this folder serves the following objectives:

1. Experiment Js2Py: evaluation/js2py
2. Use JavaScripthon to translate Atom Feature Test data
   2.1 javascripthon_translator.sh: perform translation
   2.2 javascripthon_atom_test_result/ : translation result is saved in this folder

3. Evaluation Metrics implementation:
   Token Accuracy, Program Accuracy, Edit Token Distance Accuracy(EDR)
   3.1 js_tokenizer.js: tokenized translated .js programs, save result as `xx_tokenized.txt` files, under javascripthon_atom_test_result/ folder.
   3.2 evaluate_javascripthon.py: the script performs evaluation metrics calculation and outputs scores in terminal.
4. Evaluation Metrics implementation:
   Compile Accuracy, Computational Accuracy, Atom Feature Accuracy
   4.1 get_execution_results.sh: executes .js programs and save the execution result into `.txt` files.
   4.1.1 the_output_execution.txt
   4.1.2 the_target_execution.txt
   4.2 evaluation_javascripthon.py: the script performs evaluation metrics calculation and outputs scores in terminal. It also generates two .csv files including analysis statistics of the outputs.
   4.2.1 atom_feature_analysis.csv
   4.2.2 atom_feature_distribution.csv

# JavaScripthon Translation & Evaluation Workflow

For more detial and flowchart, please check my report.

```bash
$ sh javascripthon_translator.sh
$ node js_tokenizer.js
$ python3 evaluate_javascripthon.py
```

# JavaScripthon: PY->JS

GitHub: https://github.com/metapensiero/metapensiero.pj#introduction
An online platform built on top of JavaScripthon: https://extendsclass.com/python-to-javascript.html
NOTE: Must use Python 3.5<=version<=3.8

JavaScripthon is the selected commercial translator compared with the trained Python-JavaScript Tree2Tree translator.

## installation

I highly recommend one to use anaconda to create a virtual env with a specific python version. Anaconda differs from Python virtual env to have this special feature that is very suitable to this case.

### install with conda (recommended)

```bash
sh javascripthon_translator.sh
```

### install with pip (not recommended)

```bash
pip install javascripthon
```

# JS2PY: JS->PY

Js2Py is a commercial tool to translate JavaScript into Python3.
GitHub: https://github.com/PiotrDabkowski/Js2Py
PyPi: https://pypi.org/project/Js2Py/

installation with pip:

```bash
pip install Js2Py
```
