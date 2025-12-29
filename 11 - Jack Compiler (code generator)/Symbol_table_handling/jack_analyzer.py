'''
Class for analyzing Jack programs, understanding the semantics of the symbols and generating XML output.

Individual Jack file Example usage:  
python jack_compiler.py test/ArrayTest/Main.jack

Directory Example usage:  
python jack_compiler.py test/Square

'''

from compilation_engine import CompilationEngine
import os
import argparse


def main():
    parser = argparse.ArgumentParser(description="Jack Analyzer: Tokenizes and compiles Jack files to XML.")
    parser.add_argument('input_path', help="Input .jack file or directory containing .jack files")
    args = parser.parse_args()

    analyzer = JackAnalyzer(args.input_path)
    analyzer.analyze()

class JackAnalyzer:
    def __init__(self, input_path:str):
        self.input_files: list[str] = []
        if input_path.endswith('.jack'):
            self.input_files.append(input_path)
        else:
            for file in os.listdir(input_path):
                if file.endswith('.jack'):
                    self.input_files.append(os.path.join(input_path, file))

    def analyze(self):
        '''Analyze the Jack files and generate XML output for each input file.'''
        for input_file in self.input_files:
            output_file = input_file.replace('.jack', '.xml')
            compiler = CompilationEngine(input_file, output_file)
            compiler.compile_class()


if __name__ == "__main__":
    main()