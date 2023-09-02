from module_handler import modules

modules = modules("module_engine/pickles/naive_bayes_model.pkl", "module_engine/pickles/tfidf_vectorizer.pkl", "modules/modules.json")

print("Detected module: " + modules.predict_module("I want to know about the weather"))

print(modules.use_module("Weather", "London"))