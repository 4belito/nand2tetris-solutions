"""
Class for compiling Jack programs and generating vm output.

Individual Jack file Example usage:
python jack_compiler.py test1/ArrayTest/Main.jack

Directory Example usage:
python jack_compiler.py test1/Square

"""

import argparse
import os

from compilation_engine import CompilationEngine


def main():
    parser = argparse.ArgumentParser(
        description="Jack Compiler: Compile Jack files and generate vm code."
    )
    parser.add_argument(
        "input_path", type=str, help="Path to a .jack file or a directory containing .jack files."
    )
    args = parser.parse_args()
    compiler = JackCompiler(args.input_path)
    compiler.compile()


class JackCompiler:
    def __init__(self, input_path: str):
        self.input_files: list[str] = []
        if input_path.endswith(".jack"):
            self.input_files.append(input_path)
        else:
            for file in os.listdir(input_path):
                if file.endswith(".jack"):
                    self.input_files.append(os.path.join(input_path, file))

    def compile(self):
        """Compile the Jack files and generate .vm output for each input file."""
        for input_file in self.input_files:
            output_file = input_file.replace(".jack", ".vm")
            compiler = CompilationEngine(input_file, output_file)
            compiler.compile_class()


if __name__ == "__main__":
    main()
