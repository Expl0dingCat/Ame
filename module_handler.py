import importlib
import joblib
import json
import os

class modules:
    def __init__(self, model_path, vectorizer_path, modulesjson_path) -> None:
        self.module_map = {}
        self.module_json = json.load(open(modulesjson_path, "r"))

        self.load_models(model_path, vectorizer_path)
        self.load_modules()

    def load_models(self, model_path, vectorizer_path):
        model_filename = model_path
        self.loaded_model = joblib.load(model_filename)

        vectorizer_filename = vectorizer_path
        self.vectorizer = joblib.load(vectorizer_filename)
    
    def predict_module(self, query):
        query_vector = self.vectorizer.transform([query])
        predictions = self.loaded_model.predict(query_vector)
        predicted_probabilities = self.loaded_model.predict_proba(query_vector)
        if max(predicted_probabilities[0]) < 0.7:
            return None, max(predicted_probabilities[0])
        return predictions[0], max(predicted_probabilities[0])

    def load_modules(self):
        for module_info in self.module_json:
            if module_info.get("detectable", False):
                module_name = module_info["name"]
                module_file = f"modules/{module_name}.py" 
                if os.path.isfile(module_file):
                    try:
                        module = importlib.import_module(f"modules.{module_name}")
                        self.module_map[module_name] = module
                    except ModuleNotFoundError:
                        pass

    def use_module(self, module_name, *args, **kwargs):
        module = self.module_map.get(module_name)
        if module:
            for module_info in self.module_json:
                if module_info["name"] == module_name:
                    func_name = module_info.get("function", "default_function_name")
                    func = getattr(module, func_name, None)
                    if func and callable(func):
                        return func(*args, **kwargs)
                    else:
                        return f"Function '{func_name}' not found in module '{module_name}'"
            return f"Module information for '{module_name}' not found in module_json"
        else:
            return f"Module '{module_name}' not found"

if __name__ == '__main__':
    print('This is a handler, it is not meant to be run directly.')
    pass
    

