import importlib
import os

# Untested and unfinished

class modules():
    def __init__(self) -> None:
        self.module_map = {}
        for module_name in os.listdir("modules"):
            if os.path.isdir(os.path.join("modules", module_name)):
                module_path = f"modules.{module_name}.main"
                try:
                    module = importlib.import_module(module_path)
                    self.module_map[module_name] = module
                except ModuleNotFoundError:
                    pass
        
    def get_module(self, module_name):
        return self.module_map.get(module_name, None)
    
    def use_module(self, module_name, *args, **kwargs):
        module = self.get_module(module_name)
        if module:
            return module.main(*args, **kwargs)
        else:
            return None
        
if __name__ == '__main__':
    print('This is a handler, it is not meant to be run directly.')
    pass