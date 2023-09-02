# Modules

This is the documentation for everything regarding modules. Including the module handler (`module_handler.py`), the module API in the controller and the creation of modules.

## Terminology

- `Query`: The user's request (e.g. "Whats the weather like?").
- `Single pass modules`: Modules that do not have any arguments and do not require any second passes through a LLM to extract variables from the query. (Can be detected solely by the built in module engine).
- `Double pass modules`: Modules that have arguments that need to be extracted by a second pass through a LLM. (Can be detected by the built in module engine but require a LLM for variable extraction).

## Module Handler

The module handler (`module_handler.py`) handles module importing and management. It contains a class, `modules` with 5 methods:

- **\__init()__**: `model_path`: _string_, `vectorizer_path`: _string_, `modulesjson_path`: _string_

  Initializes the class.

  - `model_path`: _string_

  The path for the model file used for module classification.
  
  - `vectorizer_path`: _string_

  The path for the vectorizer file.
  
  - `modulesjson_path`: _string_
  
  The path for the `modules.json` file.

- **load_models()**: `model_path`: _string_, `vectorizer_path`: _string_
Loads required models for `predict_module()`.
  - `model_path`: _string_
  The path for the model file used for module classification.
  
  - `vectorizer_path`: _string_
  The path for the vectorizer file.

- **predict_module()**: `query`: _string_
Predict a module using the built in classification model.
  - `query`: _string_
  The query to predict a module.

- **get_module()**: `module_name`: _string_
Get a module.

## Using modules via the API

The controller contains a method for running a module, this method is a direct call of the `use_module()` method found in the module handler.

Example:
```py
from controller import controller

# Initialize the controller, see documentation for more info

controller =  controller()

response = controller.run_module(module, args)
```

## Creating modules

Modify the `modules.json` file to add your module, it has 5 keys:

-  `id`: integer
An arbitrary number to identify a module.

-  `name`: string
Name of the module.

-  `args`: union[None, dict]
If `None` then the module will be detected using the built in `predict_module()` function found in `module_engine/module_handler.py` and handled as a `single pass module`. If `dict` then module will be detected and then it and it's arguments listed in the dictionary will be passed to LLaMA to parse the query (`double pass module`).

- `function`: string
The function that is called when the module is ran.

- `detectable`: boolean
If `True` the module is detectable via the built in classifier (see "`Training the classifier`")

Your module file (`.py`) must be in a folder titled the `name` key found inside `modules.json` and titled `main.py`.

You can train the classifier on your own module using the `train.py` script found in (`module_engine/training/train.py`), it will use the queries and labels found in the training dataset (`module_engine/training_data.csv`), ensure you add your own pairs to both the training and validation dataset (`module_engine/validation_data.csv`). If you do not understand how to do this, you can skip this step or read the section "`Training the classifier`" for more information. Skipping this will not allow for fast detection of `single pass modules`. `Double pass modules` will remain mostly uneffected.

## Training the classifier

The classifier is used for both `single pass modules` and `double pass modules`, however it is most useful for drastically speeding up `single pass modules`. In order to train your module to be detected by the built in classifier, you need to modify the training data (`module_engine/training_data.csv`) and validation data (`module_engine/validation_data.csv`) by adding additional pairs of queries and labels in a CSV format:
```
query,label
```
Example:
```
Tell me the latest finance news,News
What's the current dew point?,Weather
```
I suggest using a LLM to generate these such as ChatGPT. The training data and validation data must be different. Once you have your datasets prepared, you can start the training by running:
```
python module_engine/training/train.py
```