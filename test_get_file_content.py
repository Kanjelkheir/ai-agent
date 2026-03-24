from functions.get_file_content import get_file_content

try:
    content = get_file_content("./calculator", "./calculator/lorem.txt")
    print(content)
except Exception as e:
    print(f"Error: {e}")
