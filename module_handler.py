import importlib
import joblib
import json
import os

# Untested and unfinished

class modules:
    def __init__(self, model_path, vectorizer_path, modulesjson_path) -> None:
        self.module_map = {}
        self.module_list = json.load(open(modulesjson_path, "r"))
        self.load_models(model_path, vectorizer_path)
        for module_name in os.listdir("modules"):
            if os.path.isdir(os.path.join("modules", module_name)):
                print(module_name)
                module_path = f"modules.{module_name}"
                try:
                    module = importlib.import_module(module_path)
                    self.module_map[module_name] = module
                except ModuleNotFoundError:
                    pass
                print(self.module_map)

    def load_models(self, model_path, vectorizer_path):
        model_filename = model_path
        self.loaded_model = joblib.load(model_filename)

        vectorizer_filename = vectorizer_path
        self.vectorizer = joblib.load(vectorizer_filename)

    def predict_module(self, query):
        query_vector = self.vectorizer.transform([query])
        predictions = self.loaded_model.predict(query_vector)
        return predictions[0]

    def get_module(self, module_name):
        return self.module_map.get(module_name, None)
    
    def use_module(self, module_name, *args, **kwargs):
        module = self.get_module(module_name)
        if module:
            return module.main(*args, **kwargs)
        else:
            return None
        
if __name__ == '__main__':
    print('This is a handler, it is not meant to be run directly.')
    pass