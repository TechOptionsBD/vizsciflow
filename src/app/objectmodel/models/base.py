from .loader import Loader

class ModuleBase():
    @staticmethod
    def load(url):
        return Loader.load_funcs_recursive_flat(url)