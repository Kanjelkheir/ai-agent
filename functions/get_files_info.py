import os
import pdb

"""
Function that fetches the file info and returns them as string output
"""
def get_files_info(working_directory, directory="."):

    working_absolute_path = os.path.abspath(working_directory)
    full_path = os.path.join(working_absolute_path, directory)
    target_dir = os.path.normpath(full_path)
    if os.path.isdir(target_dir) == False:
        pdb.set_trace()
        raise Exception(f'Error: "{directory}" is not a directory')

    # Will be True or False
    valid_target_dir = os.path.commonpath([working_absolute_path, target_dir]) == working_absolute_path
    if valid_target_dir == False:
        pdb.set_trace()
        raise Exception(f'Error: Cannot list "{directory}" as it is outside the permitted working directory')

    dirs = os.listdir(target_dir)

    files = list()

    for file in dirs:
        # get and store file name
        file_size = None
        is_dir = None
        print(f"File is {file}")
        print(f"Target dir is {target_dir}")
        print(f"Target now is {os.path.join(target_dir, file)}")
        try:
            file_size = os.path.getsize(os.path.join(target_dir, file))
            is_dir: bool = os.path.isdir(os.path.join(target_dir, file))
        except Exception as e:
            pdb.set_trace()
            raise Exception(f"Error: {e}")

        data = File(name=file, size=file_size, dir=is_dir)

        files.append(data)

    output = ""
    for file in files:
        print(file.size)
        print(file.data())
        # for each file append a data string
        output.join(file.data())
        output += file.data()
        output += '\n'

    return output


