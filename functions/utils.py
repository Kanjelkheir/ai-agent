"""
File class that contains data about the file
input: name, size, dir
"""
class File:
    def __init__(self, name, size, dir):
        self.name = name
        self.size = size
        self.dir = dir

    def data(self) -> str:
        return f"- {self.name}: file_size={self.size} bytes, is_dir={self.dir}\n"

