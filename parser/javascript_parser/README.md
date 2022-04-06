# General Steps

download antlr4, set alias, set CLASSPATH
see the root folder README.

# Grammar

grammar is taken from: https://github.com/antlr/grammars-v4/tree/master/javascript

## Download Lexer and Parer Grammar + LexerBase.java

```bash
wget https://raw.githubusercontent.com/antlr/grammars-v4/master/javascript/javascript/JavaScriptLexer.g4

wget https://raw.githubusercontent.com/antlr/grammars-v4/master/javascript/javascript/JavaScriptParser.g4

wget https://raw.githubusercontent.com/antlr/grammars-v4/master/javascript/javascript/Java/JavaScriptLexerBase.java

wget https://raw.githubusercontent.com/antlr/grammars-v4/master/javascript/javascript/Java/JavaScriptParserBase.java
```

### Lexer

```bash
antlr4 JavaScriptLexer.g4
```

which creates the following files:
JavaScriptLexer.java
JavaScriptLexer.interp
JavaScriptLexer.tokens

### Parser

```bash
antlr4 JavaScriptParser.g4
```

which creates the following files:
JavaScriptParser.interp
JavaScriptParser.java
JavaScriptParser.tokens
JavaScriptParserBaseListener.java
JavaScriptParserListener.java

# Compile All Java Code

compile all the generated java source code (if get a ClassNotFoundException error from the compiler, check if the Java CLASSPATH environment variable is configured correctly)

```bash
javac *.java
```

# TreeParser: Integrate a Generated Parser into a Java Program

Write the Java Program which reads from an input file containing javascript code,
and write the parsed tree into a new file.

```bash
javac *.java //compile everything
java TreeParser javasc_train_1.js //use the TreeParser we just wrote to parse the .js code and write the parse tree into a txt file.
```

---

# If want to write TreeParser in JavaScript

download the runtime: npm or from the web
https://www.antlr.org/download/index.html
(looks like lab's npm is outdated and I don't have the permission to update it)

```bash
antlr4 -Dlanguage=JavaScript JavaScriptLexer.g4

antlr4 -Dlanguage=JavaScript JavaScriptParser.g4
```
