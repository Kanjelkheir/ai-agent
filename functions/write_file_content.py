import os

def write_file(working_directory, file_path, content):
    # check if both files are in the same directory
    working_absolute_path = os.path.abspath(working_directory)
    absolute_file_path = os.path.abspath(file_path)
    valid_dir = os.path.commonpath([working_absolute_path, absolute_file_path]) == working_absolute_path
    if valid_dir == False:
        raise Exception(f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory')
    # check if the file_path points to a file or not
    is_dir = os.path.isdir(absolute_file_path)
    if is_dir == True:
        raise Exception(f'Error: Cannot write to "{file_path}" as it is a directory')
    # check if the parent dirs of file_path exist and create them if not
    directory = os.path.dirname(absolute_file_path)
    os.makedirs(directory, exist_ok=True)
    # open the file in write mode and override the content
    with open(absolute_file_path, "w") as file:
        try:
            file.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        except Exception as e:
            print(f"Error {e}")

