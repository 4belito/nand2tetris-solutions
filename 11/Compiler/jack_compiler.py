'''Class for analyzing Jack programs and generating XML output.'''

from compilation_engine import CompilationEngine
import os
import argparse


def main():
    parser = argparse.ArgumentParser(description="Jack Compiler: Analyze Jack files and generate vm code.")
    parser.add_argument('input_path', type=str, help="Path to a .jack file or a directory containing .jack files.")
    args = parser.parse_args()
    compiler = JackCompiler(args.input_path)
    compiler.compile()


class JackCompiler:
    def __init__(self, input_path:str):
        self.input_files: list[str] = []
        if input_path.endswith('.jack'):
            self.input_files.append(input_path)
        else:
            for file in os.listdir(input_path):
                if file.endswith('.jack'):
                    self.input_files.append(os.path.join(input_path, file))

    def compile(self):
        '''Analyze the Jack files and generate XML output for each.'''
        for input_file in self.input_files:
            output_file = input_file.replace('.jack', '.vm') #.xml
            compiler = CompilationEngine(input_file, output_file)
            compiler.compile_class()


if __name__ == "__main__":
    main()