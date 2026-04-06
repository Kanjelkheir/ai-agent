import subprocess
from .utils import Model
import questionary
import ollama
from .get_files_info import get_files_info
from .get_file_content import get_file_content
from .write_file_content import write_file
from .run_python_file import run_python_file
from prompts import system_prompt

# Note: This is currently programmed only for ollama v0.18.2

"""
Gets the current models installed on Ollama
"""
def get_models():
    # Fetch the list of models
    response = ollama.list()
    models = list()    
    # Extract just the names
    for m in response['models']:
        model_full_name = m['model'].split(':')
        model_name = model_full_name[0]
        model_version = model_full_name[1]
        model = Model(model_name, model_version)
        models.append(model)

    return models

def select_local_model():
    try:
            # Get models
                Models = get_models()
                models = [f"{model.model_name}:{model.model_version}" for model in Models]
                # Ask which model the user want

                choice = questionary.select(
                    "Choose a model:",
                    choices=models
                ).ask()
                if choice is None:
                     return None

                return choice.split(':')
    except Exception as e:
        print(e)

def select_model():
        try:
            choice = select_local_model()
            if choice == None:
                print("user cancelled selection")
                exit(1)

            model_name = choice[0]
            model_version = choice[1]
            return (model_name, model_version)
        except Exception as e:
            print(e)

def call_local_model():
     history = [{'role': 'system', 'content': system_prompt}]
     available_tools = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "write_file": write_file,
        "run_python_file": run_python_file, 
     }
     def call(model: str, prompt: str):
          history.append({'role': 'user', 'content': prompt})
          
          # 2. Pass the entire history as the context
          response = ollama.chat(
               model=model, 
               messages=history, # No need to add prompt again here
               options={'think': True}, 
               tools=[get_files_info, get_file_content, write_file, run_python_file]
          )
          
          # 3. Extract the response safely
          response_message = response['message']
          response_text = response_message.get('content', '')
          
          # 4. Add the assistant response to history to maintain the loop
          history.append(response_message)

          if response_message.get('tool_calls'):
               for tool in response_message['tool_calls']:
                    print(f"Model wants to call: {tool['function']['name']}")
                    print(f"With arguments: {tool['function']['arguments']}")
               # Note: Usually you'd execute the tool here and append the result to history
                    arguments = tool['function']['arguments']
                    function_name = tool['function']['name']
                    if function_name in available_tools:
                        function_to_call = available_tools[function_name]
                        output = function_to_call(**arguments)
                        history.append({
                             'role': 'tool',
                             'content': output,
                             'name': function_name,
                        })
          else:
               print(response_text)
               exit(0)
               
     return call