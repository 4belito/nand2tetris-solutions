'''VMTranslator.py
VMTranslator.py - A simple VM translator for the Nand2Tetris project.
This script reads VM commands from a file and translates them into Hack assembly code.'''


import os
import argparse
from commands import Arithmetic, Memory


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filepath", help="vm file to read")
    args = parser.parse_args()
    file_name = os.path.splitext(os.path.basename(args.filepath.strip()))[0]
    arithmetic = Arithmetic()
    memory = Memory(file_name)
    # First pass: build symbol table and collect cleaned lines
    with open(args.filepath, "r") as f, open(f"{file_name}.asm", "w") as out_f:
        line_num = 0
        for vmline in f:
            code_only = vmline.split("//")[0]
            cmd = code_only.split()
            if not cmd:
                continue
            else:
                line_len = len(cmd)
            if line_len==1:
                text_out = arithmetic.translate(cmd[0], line_num)
            elif line_len==3:
                text_out = memory.translate(cmd[0], cmd[1], int(cmd[2]))
            else:
                raise ValueError(f"Invalid command format: {cmd}")
            out_f.write(text_out + "\n")
            line_num += 1
        print(f"Translated {args.filepath} to {file_name}.asm successfully.")
        out_f.write(arithmetic.end())   
if __name__ == "__main__":
    main()