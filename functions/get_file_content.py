import os
from google.genai import types


"""
Function that fetches the file content of a file
"""
def get_file_content(working_directory, file_path):
    file_path = os.path.join(working_directory, file_path)
    # Check if the file path is inside the working directory
    working_absolute_path = os.path.abspath(working_directory)
    print(f"Working abs path: {working_absolute_path}")
    absolute_file_path = os.path.abspath(file_path)
    print(f"Absolute file path: {absolute_file_path}")
    valid_target_dir = os.path.commonpath([working_absolute_path, absolute_file_path]) == working_absolute_path
    if valid_target_dir == False:
        raise Exception(f'Error: Cannot read "{file_path}" as it is outside the permitted working directory')

    is_file = os.path.isfile(absolute_file_path)
    if is_file == False:
        raise Exception(f'Error: File not found or is not a regular file: "{file_path}"')

    # Read 10,000 characters from the files
    with open(absolute_file_path) as file:
        content = None
        try:
            content = file.read(10_000)
            # check if the file is above 10,000 characters
            ch = file.read(1)
            if ch:
                content += f'[...File "{absolute_file_path}" truncated at 10,000 characters]'
        except Exception as e:
            print("Error: {e}")
        return content


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Get the content of a file in text format",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path relative to the working directory",
            ),
            "working_directory": types.Schema(
                type=types.Type.STRING,
                description="The working directory"
            )
        },
    ),
)
