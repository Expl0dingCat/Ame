
# Ame Module System Documentation

Welcome to the Ame Module System documentation. This guide covers everything related to modules, including the module handler (`module_handler.py`), the module API in the controller, and creating custom modules.

## Table of Contents
1. [Terminology](#terminology)
2. [Module Handler](#module-handler)
3. [Using Modules via the API](#using-modules-via-the-api)
4. [Creating Custom Modules](#creating-custom-modules)
5. [Training the Classifier](#training-the-classifier)
6. [Conclusion](#conclusion)

## 1. Terminology

To ensure clarity throughout this documentation, let's define some key terms:

- **Query**: The user's request (e.g., "What's the weather like?").
- **Single Pass Modules**: Modules that do not require any arguments and are detected solely by the built-in module engine.
- **Double Pass Modules**: Modules that have arguments requiring a second pass through a Language Model (LLM) to extract variables from the query.
- **Module Handler**: The Python script `module_handler.py` responsible for managing modules.

## 2. Module Handler

### 2.1 Initialization
**\_\_init\_\_()**: `model_path`: (string), `vectorizer_path`: (string), `modulesjson_path`: (string)
  Initializes the module handler.
  - `model_path`: (string) Path to the module classification model.
  - `vectorizer_path`: (string) Path to the vectorizer file.
  - `modulesjson_path`: (string) Path to the `modules.json` configuration file.

### 2.2 Loading Models
**load_models()**: `model_path`: (string), `vectorizer_path`: (string)
  Loads the required models for module classification.
  - `model_path`: (string) Path to the module classification model.
  - `vectorizer_path`: (string) Path to the vectorizer file.

### 2.3 Module Prediction
**predict_module()**: `query`: (string)
  Predicts a module using the built-in classification model.
  - `query`: (string) The user's query to predict a module.

### 2.4 Module Loading
**load_modules()**
  Loads the modules that are marked as `detectable`.

### 2.5 Module Usage
**use_module()**: `module_name`: (string), `*args`, `**kwargs`
  Uses a module and obtains a response from its associated function.
  - `module_name`: (string) Name of the module to use.
  - `*args`: Variable-length positional arguments.
  - `**kwargs`: Variable-length keyword arguments.

## 3. Using Modules via the API

To run a module using the API, follow these steps:

```python
from controller import Controller

# Initialize the controller
controller = Controller()

# Run a module
response = controller.run_module(module, args)
```

## 4. Creating Custom Modules

To create custom modules, modify the `modules.json` file with the following keys:

- `id`: (integer)
An arbitrary module identifier.
- `name`: (string)
Name of the module (must match module file name).
- `args`: (union[None, dict])
If `None`, the module is detected using `predict_module()` and handled as a single-pass module. If `dict`, the module is detected, and its arguments are passed to an LLM to parse the query (double-pass module).
- `function`: (string)
The function called when the module is executed.
- `detectable`: (boolean)
If `True`, the module is detectable via the built-in classifier.

Place your module file (`.py`) in the `modules` folder.

## 5. Training the Classifier

The classifier is used for both single-pass and double-pass modules. To train your module to be detected by the built-in classifier:

- Modify the training data (`module_engine/training_data.csv`) and validation data (`module_engine/validation_data.csv`) by adding pairs of queries and labels in CSV format.
- Example:
  ```
  query,label
  Tell me the latest finance news,News
  What's the current dew point?,Weather
  ```

- Use a Language Model (LLM) to generate these pairs, such as ChatGPT, or handwrite them.
- Ensure that the training data and validation data are unique.
- Start the training by running:
  ```
  python module_engine/training/train.py
  ```

## 6. Conclusion

Thank you for exploring the Ame Module System documentation. This system empowers you to create and manage custom modules seamlessly. If you have any questions or need further assistance, please don't hesitate to reach out.

For additional resources, including more documentation and support forums, visit [the discord server](https://discord.gg/S6h8XYsuZt).

