from jack_tokenizer import JackTokenizer
from compilation_engine import CompilationEngine


class JackAnalyzer:
    def __init__(self, input_text):
        self.tokenizer = JackTokenizer(input_text)
        self.compiler = CompilationEngine(self.tokenizer)

    def analyze(self):
        self.tokenizer.tokenize()
        self.compiler.compile()
        # Further analysis logic goes here
        pass
