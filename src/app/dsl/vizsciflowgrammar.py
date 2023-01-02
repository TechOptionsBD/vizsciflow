from pyparsing import *
from pyparsing import _bslash
from dsl.grammar import PythonGrammar

class VizSciFlowGrammar(PythonGrammar):
    def __init__(self):
        self.build_grammar()

    def build_program(self):
        self.stmt << Group((self.taskdefstmt | self.parstmt | self.retstmt | self.ifstmt | self.parforstmt | self.forstmt | self.lockstmt | self.funccallstmt | self.funccalls | self.assignstmt | self.expr).setParseAction(lambda s,l,t :  ['STMT'] + [lineno(l, s)] + [t]))
        self.stmtlist << ZeroOrMore(self.stmt)
        self.program = self.stmtlist

    def build_grammar(self):
        super().build_grammar()
        # parfor keyword for parallel for construct
        self.parforstmt = Group(Suppress("parfor") + self.identifier("var") + Suppress("in") + Group(self.expr("range"))  + Suppress(":") + self.compoundstmt).setParseAction(lambda t : ['PARFOR'] + t.asList())
        self.build_program()
