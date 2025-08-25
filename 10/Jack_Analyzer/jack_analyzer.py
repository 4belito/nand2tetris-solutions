'''Class for analyzing Jack programs and generating XML output.'''

from jack_tokenizer import JackTokenizer
from compilation_engine import CompilationEngine
import os

class JackAnalyzer:
    def __init__(self, input_path:str):
        if input_path.endswith('.jack'):
            self.input_files = [input_path]
        else:
            self.input_files = []
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
