import os
from dotenv import load_dotenv
from google import genai

def main():
    load_dotenv()
    try:
        api_key = get_api_key()
    except Exception as e:
        print(f"Error occured: {e}")
        exit(1)

    # create the genai client
    client = genai.Client(api_key=api_key)
    content = client.models.generate_content(model='gemini-2.5-flash', contents="hi")
    print(content.text)


def get_api_key():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("gemini api key is not found")
    return api_key


if __name__ == "__main__":
    main()
