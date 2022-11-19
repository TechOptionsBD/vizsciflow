from pyparsing import *
from pyparsing import _bslash
from dsl.grammar import PythonGrammar

class VizSciFlowGrammar(PythonGrammar):
    def __init__(self):
        self.build_grammar()
        
    def build_grammar(self):
        super().build_grammar()
        # redeclare for statement with par optional keyword for parallel for construct
        self.forstmt = Group(Suppress("for") + self.identifier("var") + Suppress("in") + Group(self.expr("range"))  + Optional(Keyword("par")) + Suppress(":") + self.compoundstmt).setParseAction(lambda t : ['FOR'] + t.asList())
        super().build_program()
