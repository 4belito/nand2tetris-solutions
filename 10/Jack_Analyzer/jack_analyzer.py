'''
Class for analyzing Jack programs and generating XML output.

Individual Jack file Example usage:  
python jack_analyzer.py test/ArrayTest/Main.jack

Directory Example usage:  
python jack_analyzer.py test/Square
'''

from jack_tokenizer import JackTokenizer
from compilation_engine import CompilationEngine
import os
import argparse

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
        '''Analyze the Jack files and generate XML output for each.'''
        for file in self.input_files:
            tokenizer = JackTokenizer(file)
            output_file = file.replace('.jack', '.xml')
            compiler = CompilationEngine(tokenizer, output_file)
            compiler.compile_class()

def main():
    parser = argparse.ArgumentParser(description="Jack Analyzer: Tokenizes and compiles Jack files to XML.")
    parser.add_argument('input_path', help="Input .jack file or directory containing .jack files")
    args = parser.parse_args()

    analyzer = JackAnalyzer(args.input_path)
    analyzer.analyze()

if __name__ == "__main__":
    main()