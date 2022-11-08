# Rockset Bulk Load + Alias Swizzle script

This is example python code that can be used as a template for your own scripts. 
Due to the complexities of error handling and parameter passing in different environments,
this code has not necessarily handled errors in a way that is appropriate for your use case


The code consists of:
- *launcher.py* which is generic code for processing a configuration file and providing simple command line arguements for key parameters
- a series of Step classes that are orchestrated in the __main__ function of the launcher in order to manifest a series of commands
- an example configuration file in *resources/config.yaml* - this file location and name can be overridden via the command line

The Step classes are designed to be modular so that they could be used in multiple plans.

Execute the launcher using:
```
python launcher.py

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         print information to the screen
  -c CONFIG, --config CONFIG
                        yaml configuration file with test parameters
```