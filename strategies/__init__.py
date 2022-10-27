from os import path, listdir
from inspect import isclass
from pkgutil import iter_modules
from importlib import import_module
from game import Game

for (_, module_name, _) in iter_modules([path.dirname(__file__)]):

    # import the module and iterate through its attributes
    module = import_module(f"{__name__}.{module_name}")
    for attribute_name in dir(module):
        attribute = getattr(module, attribute_name)

        if isclass(attribute):
            # Add the class to this package's variables
            globals()[attribute_name] = attribute


def instantiate_game_by_name(game_name, visu=False, verbose=False, wait=0) -> Game:
    return globals()[game_name](visu, verbose, wait)
