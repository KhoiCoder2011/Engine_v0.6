import importlib.util
import sys


def import_from_path(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


class Script:
    def __init__(self, class_name: str = '', path: str = ''):
        self.obj = None
        self.app = None
        self.script = import_from_path(class_name, path)

    def start(self):
        self.script.start(self.app, self.obj)

    def update(self):
        self.script.update(self.app, self.obj)


class BlankScript:
    def __init__(self):
        self.obj = None

    def start(self):
        pass

    def update(self):
        pass
