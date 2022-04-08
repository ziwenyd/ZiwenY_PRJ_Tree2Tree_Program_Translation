# author: Ziwen Yuan

# This shell file executes a folder of translated JavaScript atom test result;
# and save the execution result into a .txt file under /evaluation/.

# In this project, this shell only used for JavaScripthon translation result,
# because the result of Tree2Tree can not even form an actual program.
# JavaScripthon only translate Python into JavaScript, so this shell only 
# executes JavaScript files.

# However, this shell can be used universally to execute any files(Python, JavaScript, 
# etc.) including a function with the logic used in this shell.
#############################################

if [ "$1" = "output" ]; # take command line argument
then 
    result_dir=the_output_execution.txt
    folder=javascripthon_atom_test_result/*.js
elif [ "$1" = "target" ]
then 
    result_dir=the_target_execution.txt
    folder=../parser/data/atom_test_data/js/*.js
else
    echo "Please provide an argument, choose from [output, target]."
    exit 1
fi

# a temporary file used to execute functions across files
touch temporary.js

: > $result_dir #clear previous content 

for i in $folder;
do cp "$i" temporary.js ; #copy content into temporary.js
echo "" >> temporary.js; #add a new line
echo "Processing ""$i"; #log current file
echo "console.log(atomTest())" >> temporary.js; #add function call
count=${i//[!0-9]/}; #get the file number
count="<FILE>${count}" #add special<FILE> token
echo "$count";
echo "$count" >> $result_dir; #write file number 

#execution result; 
#should be what returned from the function if it runs successfully.
execution_result=$(node temporary.js 2>&1); 
# only save the 5th line of error message
# e.g. TypeError: a.index is not a function
short_error_message=$(node temporary.js 2>&1 | sed -n 5p); 
if [[ "$short_error_message" == *"Error"* ]]; 
then echo "$short_error_message" >> $result_dir;
else echo "$execution_result" >> $result_dir;
fi;
done

# delete the temporary file
rm -rf temporary.js

