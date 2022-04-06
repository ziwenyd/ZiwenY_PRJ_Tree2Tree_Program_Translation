# author: Ziwen Yuan
# This shell script:
#  1) create a conda env with Python v3.6 to experiment with JavaScripthon.
#  2) install javascripthon in the conda env
#  3) translate all atom tests using JavaScripthon
#  4) clean up translation result for future use.

## install conda, steps can be found in 
## https://docs.conda.io/projects/conda/en/latest/user-guide/install/macos.html
conda -V # check conda version to make sure it is installed
#conda update conda # check conda is up-to-date

## create conda virtual env with Python3.6
# conda create -n javascripthon python=3.6 
source activate javascripthon #activate the virtual env
# conda install -c conda-forge javascripthon
# python3 -m metapensiero.pj javascripthon_test.py # translate one single file

echo "Conda env is activated with Python 3.6"
echo "This shell script translates Atom Test dataset from Python to JavaScript"
pj -o javascripthon_atom_test_result/ ../parser/data/atom_test_data/py
echo "Translation finished. Result saved in folder javascripthon_atom_test_result/"

# delete .map files 
for i in javascripthon_atom_test_result/*.map; do rm -f "$i"; done
echo "Deleted un-used translated .map files to clean up folder."

for i in javascripthon_atom_test_result/*.js; do sed -i '' -e '$ d' "$i"; done
echo "Removed the last comment line of all translated .js files."

conda deactivate # deactivate the env
echo "Deactivated conda env."