from functions.ollama import get_models

def test_get_models():
    models = get_models()
    for model in models:
        print(model)

test_get_models()
