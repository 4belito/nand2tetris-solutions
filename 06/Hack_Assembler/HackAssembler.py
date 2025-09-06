
"""
HackAssembler: Translates Hack assembly (.asm) files into binary machine code (.hack).
This script is part of the solution for Project 6 from the Nand to Tetris course. 
    https://www.coursera.org/learn/build-a-computer
Performs two-pass processing: the first to resolve symbols and labels, the second to generate binary code.
"""


import os
import argparse
from hack_code import Code
from symbol_table import symbol_table


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filepath", help="assembly file to read")
    args = parser.parse_args()
    file_name = os.path.splitext(args.filepath.strip())[0]

    cleaned_lines: list[str] = []
    line_number = 0

    # First pass: build symbol table and collect cleaned lines
    with open(args.filepath, "r") as f:
        for line in f:
            code_only = line.split("//")[0]
            cleaned = "".join(code_only.split())
            if not cleaned:
                continue
            if cleaned.startswith("(") and cleaned.endswith(")"):
                symbol = cleaned[1:-1]
                symbol_table[symbol] = line_number
            else:
                cleaned_lines.append(cleaned)
                line_number += 1

    # Second pass: translate to binary
    n = 16
    with open(f"{file_name}.hack", "w") as out_f:
        for line in cleaned_lines:
            if line.startswith("@"):
                address = line[1:]
                if not address.isdigit():
                    if address not in symbol_table:
                        symbol_table[address] = n
                        n += 1
                    address = symbol_table[address]
                binary = Code.translate_A(address)
            else:
                binary = Code.translate_C(line)
            out_f.write(binary + "\n")

if __name__ == "__main__":
    main()