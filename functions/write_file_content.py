import os
from google.genai import types

def write_file(working_directory, file_path, content):
    file_path = os.path.join(working_directory, file_path)
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

schema_write_file_content = types.FunctionDeclaration(
    name="write_file",
    description="Write a new content of the file, it also overrides it",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "content": types.Schema(
                type=types.Type.STRING,
                description="The new content to be written to the file",
            ),
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path of the file to be written to relative to the working directory"
            ),
            "working_directory": types.Schema(
                type=types.Type.STRING,
                description="The working directory"
            )
        },
    ),
)
