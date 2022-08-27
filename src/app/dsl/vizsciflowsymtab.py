from dsl.symtab import SymbolTable

class VizSciFlowSymbolTable(SymbolTable):
    '''
    Table to hold program symbols (vars).
    For local symbols, a stack of symbol tables is
    maintained.
    '''
    def __init__(self):
        '''
        Initializes the table.
        '''
        self.vars = {}
        
    def add_var(self, name, value):
        '''
        Adds/Overwrites a variable to the symbol table.
        :param name:
        :param value:
        '''
            
        self.vars[name] = value
        return self.get_var(name)
    
    def update_var(self, name, value):
        '''
        Updates a variable in the symbol table
        :param name:
        :param value:
        '''
        self.check_var(name)
        self.vars[name] = value
        return value