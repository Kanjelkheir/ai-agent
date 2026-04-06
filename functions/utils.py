import questionary

"""
File class that contains data about the file
input: name, size, dir
"""

class Model:
    def __init__(self, model_name, model_version):
        self.model_name = model_name
        self.model_version = model_version
    def info(self):
        print(f"Model name: {self.model_name}")
        print(f"Model version: {self.model_version}")
    
class File:
    def __init__(self, name, size, dir):
        self.name = name
        self.size = size
        self.dir = dir

    def data(self) -> str:
        return f"- {self.name}: file_size={self.size} bytes, is_dir={self.dir}\n"

