import json
from platformdirs import user_config_dir
import os
from pathlib import Path

app_name = "ai_agent"
app_author = "Bilal Kanjelkheir"
target_dir = user_config_dir(appname=app_name, appauthor=app_author)
target_file = target_dir + '/' + "settings.json"
file_path = Path(target_file)
file_path.parent.mkdir(parents=True, exist_ok=True)


def change_to_local(model_name: str, model_version: str):
    settings = {
        "model_type": "local",
        "model_name": model_name,
        "model_version": model_version,
    }


    try:
        with open(target_file, "w") as f:
            json.dump(settings, f)
    except Exception as f:
        print(f"Error: {f}")

def change_to_cloud():
    settings = {
        "model_type": "cloud",
        "model_name": "Gemini",
        "model_version": "default", 
    }

    try:
        with open(target_file, "w") as f:
            json.dump(settings, f)
    except Exception as f:
        print(f"Error: {f}")

def read_settings():


    try:
        with open(target_file, "r") as f:
            data = json.load(f)
            return (data["model_type"], data["model_name"], data["model_version"])
    except Exception as e:
        print(f"Error: {e}")