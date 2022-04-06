# General Steps

download antlr4, set alias, set CLASSPATH
see the root folder README.

# Grammar

https://github.com/antlr/grammars-v4/tree/master/python/python3

## Download Lexer and Parer Grammar + LexerBase.java

```bash
wget https://raw.githubusercontent.com/antlr/grammars-v4/master/python/python3/Python3Parser.g4
```

```bash
wget https://raw.githubusercontent.com/antlr/grammars-v4/master/python/python3/Python3Lexer.g4
```

### Lexer

```bash
antlr4 Python3Lexer.g4
```

which generates following files:
Python3Lexer.java
Python3Lexer.interp
Python3Lexer.tokens

### Parser

```bash
antlr4 Pypthon3Parser.g4
```

which generates following files:
Python3Parser.java
Python3Parser.interp
Python3ParserBaseListener.java
Python3ParserListener.java
Python3Parser.tokens

### LexerBase.java

download the Python3LexerBase.java from github

```bash
wget https://raw.githubusercontent.com/antlr/grammars-v4/master/python/python3/Java/Python3LexerBase.java
```

# Compile All Java Code

compile all the generated java source code (if get a ClassNotFoundException error from the compiler, check if the Java CLASSPATH environment variable is configured correctly)

```bash
javac *.java
```

# Test with grun -tokens and -gui

## -tokens

Test the Generated parser, print out the tokens created by the lexer:

```bash
$ grun Python3 single_input -tokens
x=1
EoF #(end of file), ctrl+D on Unix and ctrl+Z on Windows
[@0,0:0='x',<NAME>,1:0]
[@1,1:1='=',<'='>,1:1]
[@2,2:2='1',<NUMBER>,1:2]
[@3,3:3='\n',<NEWLINE>,2:0]
[@4,4:3='<EOF>',<EOF>,2:0]
```

## -gui

A window with the generated parse tree should pop up.

```bash
$ grun Python3 single_input -gui
x=1
EoF #ctrl+D on Unix
```

# IDE(VSCode) Configuration

configure classpath for java project in VSCode

1. install and enable latest VSCode Java extention
2. set a folder (not file) to be java project, then in the left panel there should be a foler called 'Referenced Libraries' where you can add the jar file to the CLASSPATH

# TreeParser: Integrate a Generated Parser into a Java Program

1. wrote program: Test.java
   (set classpath, import java runtimes)
2. test in terminal

```bash
$ javac Test.java //compile
$ java Test // run it
x=1
//EOF (ctrl+D on linux)
(single_input (simple_stmt (small_stmt (expr_stmt (testlist_star_expr (test (or_test (and_test (not_test (comparison (expr (xor_expr (and_expr (shift_expr (arith_expr (term (factor (power (atom_expr (atom x)))))))))))))))) = (testlist_star_expr (test (or_test (and_test (not_test (comparison (expr (xor_expr (and_expr (shift_expr (arith_expr (term (factor (power (atom_expr (atom 1)))))))))))))))))) \n))

```

---

# Note when creating Data

1. must at a line break(new line) at the end of the file, otherwise ANTLR will encounter an error like this, this is due to the design of the Python grammar we use for the python parser.

```bash
line 1:3 mismatched input '<EOF>' expecting {NEWLINE, ';'}
```
