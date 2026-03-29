import os
import subprocess
from typing import List
from google.genai import types

def run_python_file(working_directory, file_path, args=None):
    print(type(args))
    file_path = os.path.join(working_directory, file_path)
    # check if the file path is in the working directory
    working_absolute_path = os.path.abspath(working_directory)
    absolute_file_path = os.path.abspath(file_path)
    print(absolute_file_path)
    valid_target_dir = os.path.commonpath([working_absolute_path, absolute_file_path])
    if valid_target_dir == False:
        raise Exception(f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory')
    # make sure the file_path points to a file and not a dir
    is_file = os.path.isfile(absolute_file_path)
    if is_file == False:
        raise Exception(f'Error: "{file_path}" does not exist or is not a regular file')
    # check if file name ends with '.py'
    file_extension = os.path.normpath(absolute_file_path)[-3:]
    if file_extension != '.py':
        print(f"File extension: {file_extension}")
        raise Exception(f'Error: "{file_path}" is not a Python file')

    # use subprocess to run the command
    result = ""
    try:
        print(absolute_file_path)
        if args is None:
            command: List[str] = ["python", absolute_file_path]
        else:
            command: List[str] = ["python", absolute_file_path] + args
        output = subprocess.run(command, capture_output=True, text=True, timeout=30)
        # check the return code of the command
        return_code = output.check_returncode()
        if return_code != 0:
            result += f"Process exited with code {return_code}\n"
        # check if output is produced
        if output.stdout == "" and output.stderr == "":
            result += "No output produced"
        else:
            result += f"STDOUT: {output.stdout}\n"
            result += f"STDERR: {output.stderr}\n"
        return result
    except Exception as e:
        print(f"Error executing python file: {e}")


schema_run_python_file=types.FunctionDeclaration(
    name="run_python_file",
    description="Run python file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "args": types.Schema(
                type="ARRAY",
                items=types.Schema(
                    type="STRING",
                ),
                description="The arguments to be passed to the python file",
            ),
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path for which is going to be executed"
            ),
            "working_directory": types.Schema(
                type=types.Type.STRING,
                description="The working directory"
            )
        },
    ),
)
