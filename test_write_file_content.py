from functions.write_file_content import write_file

try:
    message = write_file("./calculator", "./calculator/lorem.txt", "wait, this isn't lorem ipsum")
    print(message)
except Exception as e:
    print(e)
