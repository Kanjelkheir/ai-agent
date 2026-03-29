from functions.run_python_file import run_python_file

try:
    output = run_python_file(working_directory="calculator", file_path="main.py", args="3 + 5")
    print(output)
except Exception as e:
    print(e)
