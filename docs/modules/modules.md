# Module usage

This is the documentation for everything regarding modules. Including the module handler, the module API in the controller and the creation of modules.


## Module Handler

The module handler (`module_engine/module_handler.py`) hanldes module importing and management.

It contains a class, `modules` with 5 methods:

- **\__init()__**: `model_path`: _string_, `validation_path`: _string_, `modulesjson_path`: _string_
  - `model_path`: string
  The path for the model file used for single pass modules.
  
  - `tokenizer_path`: string
  The path for the tokenizer file.
  
  - `modulesjson_path`: string
  The path for the `modules.json` file.

- **load_models**: 

## Using modules via the API

The controller contains a method for running a module, this method is a direct call to 

Example:
```py
from controller import controller

# Initialize the controller, see documentation for more info

controller =  controller()
module_name = ""
# Generate text based on the input "Hello, World!"

response = controller.run_module(module, args)
```

## Creating modules

Modify the `modules.json` file to add your module, it has 3 keys:

-  `id`: integer
An arbitrary number to identify a module.

-  `name`: string
Name of the module.

-  `args`: union[None, dict]
If `None` then the module will be detected using the built in `predict_module_single()` function found in `module_engine/module_handler.py` without any second passes. If `dict` then module will be detected and then it and it's arguments listed in the dictionary will be passed to LLaMA to parse the query.

- `function`: string
The function that is called when the module is ran.

Your module file (`.py`) must be in a folder titled the `name` key found inside `modules.json` and titled `main.py`.

