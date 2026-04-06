import os
import sys
import dotenv
from google import genai
from google.genai import types
from functions.call_functions import available_functions, call_function
from functions.ollama import get_models, select_model
from functions.utils import Model
import argparse
import prompts
from settings import change_to_cloud, change_to_local, read_settings
from functions.ollama import call_local_model
import json


def main():
    parser = argparse.ArgumentParser(description="An ai agent cli tool written in python")
    parser.add_argument("prompt", type=str, help="The prompt sent to the ai agent", nargs='?')
    parser.add_argument("--config", action="store_true", help="Edit the ai_agent configuration")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    prompt = args.prompt

    if (prompt == "" or prompt is None) and args.config == False:
        print("Prompt is empty, please provide a prompt!")
        sys.exit(1)

    messages = [types.Content(role="user", parts=[types.Part(text=prompt)])]

    if args.config == True:
        model_type = input("Choose local or cloud model: [L/C] ").lower()
        if model_type == 'l':
            # Ask the user which model he wants
            try:
                model_name, model_version = select_model()
                model = Model(model_name, model_version)
            # Change settings.json 
                change_to_local(model_name, model_version)
            except Exception as e:
                print(e)
                sys.exit(1)

        elif model_type == 'c':
            # Prompt for Gemini api key
            try:
                api_key = input("Enter your Gemini API key (from aistudio): ")
                change_to_cloud()
                # set the api key
                dotenv.set_key(".env", "GEMINI_API_KEY", api_key)
            except Exception as e:
                print(e)
                sys.exit(1)
        else:
            print("Error, invalid input")
            sys.exit(1)
        sys.exit(0)


    # Check if local model is selected in settings.json
    try:
        settings = read_settings()
        if settings:
           model_type, model_name, model_version = settings 
           if model_type == "local":
            runtime = call_local_model()
            current_prompt = prompt
            while True:
                runtime(model_name, current_prompt)
    except Exception as e:
        print(e)


    print("finished loop")
    try:
        api_key = get_api_key()
    except Exception as e:
        print(f"Error occured: {e}")
        sys.exit(1)

      
    # create the genai client
    try:
        client = genai.Client(api_key=api_key)
        system_prompt = prompts.gemini_prompt
        config=types.GenerateContentConfig(system_instruction=system_prompt, tools=[available_functions])
        for i in range(20):
            response  = client.models.generate_content(model='gemini-2.5-flash', contents=messages, config=config)
            
            function_calls = response.function_calls
            if response.candidates == None:
                print("Unable to get candidates content")
                sys.exit(1)
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
                sys.exit(1)

    except Exception as e:
        print(f"Error {e}")


def get_api_key():
    dotenv.load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("gemini api key is not found")
    return api_key


if __name__ == "__main__":
    main()
