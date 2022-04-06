/*
author: Ziwen Yuan

This script is used to analyze JavaScript raw Programs and 
print desired statistics in terminal for observation.

This script uses an open-sourced JavaScript tokenizer, which is 
written in JavaScript - this is also why I wrote this JavaScript program 
to analyze statistics instead of a Python program.

The tokenizer requires installation.
https://github.com/lydell/js-tokens
npm install js-tokens
*/


const fs = require('fs')
const jsTokens = require("js-tokens");

const folder = 'data/train_data/'
const dataset = 'train'
const lang = 'js'

var count = 1
var file_name = folder + lang +'/'+ lang+'_'+dataset+'_'+count+'.'+lang
var total_tokens = []
var total_token_num = 0 

while (true){
    try {
        const data = fs.readFileSync(file_name, 'utf8')
        const tokens = Array.from(jsTokens(data));
        if (tokens.length == 0){
            console.log('Finished. Stopped at empty file '+file_name)
            break
        }
        var file_tokens = []
        for (token of tokens){
            var token_string = token.value
            if (token.value == ""){
                token_string = 'EMPTY_STRING'
            }
            else if (token.value == ' '){
                token_string = 'Space'
            }
            else if (token.type == 'WhiteSpace'){
                token_string = token_string.replace(/\s{4}/g, 'TAB')
            }
            file_tokens.push(token_string)
            total_tokens.push(token_string)
        }

        total_token_num += file_tokens.length

        count = count + 1
        file_name = folder + lang +'/'+ lang+'_'+dataset+'_'+count+'.'+lang
        if (! fs.existsSync(file_name)) {
            console.log('Finished. Stopped at non-exist file '+file_name)
            break
        }
      } catch (err) {
        console.error(err)
      }
}

count = count -1
var total_unique_tokens = []
for (token of total_tokens){
    if (!total_unique_tokens.includes(token)){
        total_unique_tokens.push(token)
    }
}
var total_token_num = total_tokens.length
var average_program_length = "This script does not generate this info.Please use another one."
var average_token_num = total_token_num / count

console.log('folder = '+folder+'; dataset='+dataset+'; language='+lang )
console.log('Total Program Num:', count)
console.log('Average Program Length per Program:', average_program_length)
console.log('Average Token Num per Program:', average_token_num)
console.log('All Unique Token Num across Programs:', total_unique_tokens.length)
console.log('FINISHED')