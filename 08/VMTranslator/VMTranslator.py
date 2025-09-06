'''VMTranslator.py
This script translates VM commands into Hack assembly code.
It uses the Parser class to read VM commands and the CodeWriter class to write the corresponding assembly code.
It takes a VM file as input and generates an assembly file with the same name but with a .asm extension.'''


import argparse
from parser import Parser, CMDType
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
                    case CMDType.C_ARITHMETIC:
                        writer.write_arithmetic(vm_parser.keyword)
                    case CMDType.C_PUSH | CMDType.C_POP:
                        writer.write_push_pop(cmd_type, vm_parser.arg1(), vm_parser.arg2())
                    case CMDType.C_LABEL:
                        writer.write_label(vm_parser.arg1())
                    case CMDType.C_GOTO:
                        writer.write_goto(vm_parser.arg1())
                    case CMDType.C_IF:
                        writer.write_if(vm_parser.arg1())
                    case CMDType.C_FUNCTION:
                        writer.write_function(vm_parser.arg1(), vm_parser.arg2())
                    case CMDType.C_RETURN:
                        writer.write_return()
                    case CMDType.C_CALL:
                        writer.write_call(vm_parser.arg1(), vm_parser.arg2())
                    case _:
                        raise ValueError(f"Unknown command type: {cmd_type}")

    writer.close()
    print(f"✅ Translated {filepath} successfully.")


if __name__ == "__main__":
    main()