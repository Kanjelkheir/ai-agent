from functions.write_file_content import write_file

try:
    message = write_file("calculator", "lorem.txt", "it is working!")
    print(message)
except Exception as e:
    print(e)
