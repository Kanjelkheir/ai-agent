from functions.get_files_info import get_files_info

try:
    files_info = get_files_info("calculator", "pkg")
    print(files_info)
except Exception as e:
    print(e)
