import sys
import os
import subprocess
import tempfile
import shutil
import glob
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), "build"))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), "src"))
current_dir = os.path.dirname(os.path.abspath(__file__))
build_dir = os.path.join(current_dir, 'build')
runtime_dir = os.path.join(current_dir, "src", "runtime")
sys.path.append(build_dir)
from antlr4 import *
from build.OPLangLexer import OPLangLexer
from build.OPLangParser import OPLangParser
from src.utils.error_listener import NewErrorListener
from src.astgen.ast_generation import ASTGeneration
from src.semantics.static_checker import StaticChecker
from src.utils.nodes import *
from src.codegen.codegen import CodeGenerator


sys.path.append(os.path.dirname(__file__))
def compile_and_run(ast):
    codegen = CodeGenerator() 
    # cleanup runtime file before running, finding all j and class file and remove them
    for ext in ["*.j", "*.class"]:
            files = glob.glob(os.path.join(runtime_dir, ext))
            for f in files:
                if "io.class" not in f and "jasmin.jar" not in f:
                    try:
                        os.remove(f)
                    except OSError:
                        pass
    original_dir = os.getcwd() # move to runtime file
    os.chdir(runtime_dir)
    try:
        codegen.visit(ast)
    finally:
        os.chdir(original_dir)                      
    j_files = glob.glob(os.path.join(runtime_dir, "*.j"))
        
    if not j_files:
        return "Error: No .j files generated"
    try:
        main_class = None
        for j_file in j_files:
            # Compile each file
            result = subprocess.run(
                ["java", "-jar", "jasmin.jar", os.path.basename(j_file)],
                cwd=runtime_dir,
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode != 0:
                return f"Assembly error for {os.path.basename(j_file)}: {result.stderr}"
            current_class_name = os.path.basename(j_file).replace(".j", "")
            try:
                with open(j_file, "r") as f:
                    content = f.read()
                    if ".method public static main" in content:
                        main_class = current_class_name
            except Exception:
                pass

        if not main_class:
            return "Error: No main class found"
        
        result = subprocess.run(
            ["java", main_class],
            cwd=runtime_dir,
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode != 0:
            return f"Runtime error: {result.stderr}"
        
        return result.stdout.strip()
        
    except subprocess.TimeoutExpired:
        return "Timeout"
    except FileNotFoundError:
        return "Java not found"
def main(input_file, output_file):
    input_stream = FileStream(input_file)
    lexer = OPLangLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = OPLangParser(stream)
    tree = parser.program()

    ast_gen = ASTGeneration()
    ast = ast_gen.visit(tree)

    checker = StaticChecker()
    checker.check_program(ast) 

    output = compile_and_run(ast)    
    with open(output_file, "w") as f:
        f.write(output)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python compiler_main.py <input_file> <output_dir>")
        sys.exit(1)
    
    try:
        main(sys.argv[1], sys.argv[2])
    except Exception as e:
        print(str(e))
        sys.exit(1)