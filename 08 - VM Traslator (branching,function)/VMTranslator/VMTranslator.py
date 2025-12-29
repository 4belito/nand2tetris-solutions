'''VMTranslator.py
This script translates VM commands into Hack assembly code.
It uses the Parser class to read VM commands and the CodeWriter class to write the corresponding assembly code.
It takes a VM file as input and generates an assembly file with the same name but with a .asm extension.

Example usage:
    python3 VMTranslator.py test/FunctionCalls/FibonacciElement/Main.vm

'''


import argparse
from parser import Parser, CMD
from codewriter import CodeWriter
import os

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filepath", help="vm file to read")
    args = parser.parse_args()
    filepath: str = args.filepath
    if filepath.endswith(".vm"):
        output_filepath = filepath.replace(".vm", ".asm")
        filepath = os.path.dirname(filepath)
    else:
        output_filepath = filepath + "/Sys.asm"
    writer = CodeWriter(output_filepath)
    for f in os.listdir(filepath):
        if f.endswith(".vm"):
            vm_parser = Parser(os.path.join(filepath, f))
            writer.set_file_name(file_name=os.path.splitext(f)[0])
            while vm_parser.has_more_commands():
                vm_parser.advance()
                cmd_type = vm_parser.command_type()
                match cmd_type:
                    case CMD.ARITHMETIC:
                        writer.write_arithmetic(vm_parser.keyword)
                    case CMD.PUSH | CMD.POP:
                        writer.write_push_pop(cmd_type, vm_parser.arg1(), vm_parser.arg2())
                    case CMD.LABEL:
                        writer.write_label(vm_parser.arg1())
                    case CMD.GOTO:
                        writer.write_goto(vm_parser.arg1())
                    case CMD.IF_GOTO:
                        writer.write_if(vm_parser.arg1())
                    case CMD.FUNCTION:
                        writer.write_function(vm_parser.arg1(), vm_parser.arg2())
                    case CMD.RETURN:
                        writer.write_return()
                    case CMD.CALL:
                        writer.write_call(vm_parser.arg1(), vm_parser.arg2())
                    case _:
                        raise ValueError(f"Unknown command type: {cmd_type}")

    writer.close()
    print(f"✅ Translated {filepath} successfully.")


if __name__ == "__main__":
    main()