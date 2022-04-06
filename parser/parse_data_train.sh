python3 validate_python.py
cd python_parser
javac *.java
for i in ../data/train_data/py/*.py; do java TreeParser "$i"; done
cd ..
cd javascript_parser
javac *.java
for i in ../data/train_data/js/*.js; do java TreeParser "$i"; done
echo "parsed all training data, saved the parse tree(string format) in the same foler"