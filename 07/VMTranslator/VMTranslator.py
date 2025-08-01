'''VMTranslator.py
This script translates VM commands into Hack assembly code.
It uses the Parser class to read VM commands and the CodeWriter class to write the corresponding assembly code.
It takes a VM file as input and generates an assembly file with the same name but with'''


import argparse
from parser import Parser
from codewriter import CodeWriter

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filepath", help="vm file to read")
    args = parser.parse_args()
    filepath = args.filepath
    output_file = filepath.replace(".vm", ".asm")
    vm_parser = Parser(filepath)
    writer = CodeWriter(output_file)

    while vm_parser.has_more_commands():
        vm_parser.advance()
        cmd_type = vm_parser.command_type()
        match cmd_type:
            case "C_ARITHMETIC":
                writer.writeArithmetic(vm_parser.keyword)
            case "C_PUSH" | "C_POP":
                writer.writePushPop(vm_parser.keyword, vm_parser.arg1(), vm_parser.arg2())

    writer.close()
    print(f"Translated from {filepath} to {output_file} successfully.")


if __name__ == "__main__":
    main()