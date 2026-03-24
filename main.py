import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import argparse


def main():
    parser = argparse.ArgumentParser(description="An ai agent cli tool written in python")
    parser.add_argument("prompt", type=str, help="The prompt sent to the ai agent")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    prompt = args.prompt

    messages = [types.Content(role="user", parts=[types.Part(text=prompt)])]


    load_dotenv()
    try:
        api_key = get_api_key()
    except Exception as e:
        print(f"Error occured: {e}")
        exit(1)

    # create the genai client
    client = genai.Client(api_key=api_key)
    content = client.models.generate_content(model='gemini-2.5-flash', contents=messages)
    if args.verbose:
        print(f"User prompt: {prompt}")
        print(f"Prompt tokens: {content.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {content.usage_metadata.candidates_token_count}")
    print(content.text)


def get_api_key():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("gemini api key is not found")
    return api_key


if __name__ == "__main__":
    main()
