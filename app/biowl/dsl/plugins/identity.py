from app.biowl.dsl.pluginmgr import PluginItem

class Identity(PluginItem):
    """This plugin is just the identity function: it returns the argument
    """
    def __init__(self):
        super().__init__()
        self.description = 'Identity function'

    def perform_operation(self, argument):
        """The actual implementation of the identity plugin is to just return the
        argument
        """
        return argument