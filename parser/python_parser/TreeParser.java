import org.antlr.v4.runtime.*;
import org.antlr.v4.runtime.tree.*;
import java.io.FileWriter;
import java.io.IOException;

public class TreeParser {
    public static void main(String[] args) throws Exception {
        // read from the standard input
        CharStream fileInput = CharStreams.fromFileName(args[0]);
        Python3Lexer lexer = new Python3Lexer(fileInput);
        CommonTokenStream tokens = new CommonTokenStream(lexer);
        Python3Parser parser = new Python3Parser(tokens);

        // begin parsing at the single_input rule.
        ParseTree tree = parser.single_input();
        String tree_string = tree.toStringTree(parser);

        // write the result into a new file
        try {
            int start_idx = args[0].lastIndexOf('/');
            int end_idx = args[0].length() - 3;
            String fileDir = args[0].substring(0, start_idx - 2);
            String fileName = fileDir + "py_ast_str"
                    + args[0].substring(start_idx, end_idx)
                    + "_ast_str.txt";
            FileWriter file = new FileWriter(fileName);
            file.write(tree_string);
            file.close();
            System.out.println("File Wrote: " + fileName);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
