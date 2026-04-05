from functions.ollama import get_models

def test_get_models():
    try:
        models = get_models()
        for model in models:
            model.info()
    except Exception as e:
        print(f"Error: {e}")

test_get_models()
