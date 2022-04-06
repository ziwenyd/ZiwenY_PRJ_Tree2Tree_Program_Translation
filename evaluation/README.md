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
