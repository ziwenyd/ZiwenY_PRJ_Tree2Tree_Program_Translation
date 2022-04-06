python3 validate_python.py --folder validation_data
cd python_parser
javac *.java
for i in ../data/validation_data/py/*.py; do java TreeParser "$i"; done
cd ..
cd javascript_parser
javac *.java
for i in ../data/validation_data/js/*.js; do java TreeParser "$i"; done
echo "parsed all validation data, saved the parse tree(string format) in the same foler"