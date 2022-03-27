from app.objectmodel.provmod.pluginmgr import PluginItem

class DemoProvenance(PluginItem):
    """This plugin is just the demo function: it returns the argument
    """
    def __init__(self):
        super().__init__()
        self.description = 'Demo provenance function'

    def perform_operation(self, argument):
        """The actual implementation of the demoprov plugin is to just return the
        argument
        """
        return argument