import os

def is_path_secure(path,base_directory='.'):
    base_dir = os.path.abspath(base_directory)
    absolute_path = os.path.abspath(os.path.join(base_dir, path))

    return os.path.commonpath([base_dir]) == os.path.commonpath([base_dir, absolute_path])
