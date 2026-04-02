import subprocess

def get_models():
    models = list()
    command = ["ollama", "list"]
    result = subprocess.run(command, capture_output=True, text=True).stdout
    result = result.split("\n")[1:]
    for model in result:
        if not model.strip():
            continue

        try:
            model_structure = {
                "model_name": model.split()[0].split(':')[0],
                "model_version": model.split()[0].split(':')[1]
            }
            models.append(model_structure)
            print(type(model))
        except Exception as e:
            print(f"Error: {e}")
    return models
