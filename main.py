import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.call_functions import available_functions, call_function
import argparse
import prompts



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
    try:
        client = genai.Client(api_key=api_key)
        system_prompt = prompts.system_prompt
        config=types.GenerateContentConfig(system_instruction=system_prompt, tools=[available_functions])
        for i in range(20):
            response  = client.models.generate_content(model='gemini-2.5-flash', contents=messages, config=config)
            
            function_calls = response.function_calls

            messages.append(response.candidates[0].content)

            if args.verbose:
                print(f"User prompt: {prompt}")
                print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
                print(f"Response tokens: {response.usage_metadata.candidates_token_count}")



            if function_calls:
                function_results = list()

                for function_call in function_calls:
                    function_call_result = call_function(function_call)
                    if function_call_result.parts in [[], None]:
                        raise Exception("Parts field in function_call_result is empty")
                    function_response = function_call_result.parts[0].function_response
                    if function_response == None:
                        raise Exception("Function response is None")
                    if function_response.response == None:
                        raise Exception("Response is None")
                    function_results.append(function_call_result.parts[0])

                    if args.verbose:
                        print(f"-> {function_call_result.parts[0].function_response.response}")

                messages.append(types.Content(role="tool", parts=function_results))


            else:
                print(response.text)
                break
            if i == 20:
                print("The model reached the limit of 20 messages")
                exit(1)

    except Exception as e:
        print(f"Error {e}")


def get_api_key():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("gemini api key is not found")
    return api_key


if __name__ == "__main__":
    main()
