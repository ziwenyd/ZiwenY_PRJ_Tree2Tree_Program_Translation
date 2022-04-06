python3 validate_python.py --folder atom_test_data
cd python_parser
javac *.java
for i in ../data/atom_test_data/py/*.py; do java TreeParser "$i"; done
cd ..
cd javascript_parser
javac *.java
for i in ../data/atom_test_data/js/*.js; do java TreeParser "$i"; done
echo "parsed all data/atom_test_data data, saved the parse tree(string format) in the same folder"