from typing import Callable
from types import MethodType

# Fonction permettant de servir d'initiateur aux objets.
def init(self, *args, **kwargs) -> None:
    for index, arg in enumerate(args):
        setattr(self, "arg%s" % index, arg)
    for key, value in kwargs.items():
        setattr(self, key, value)
    return

# Fonction permettant de créer des méthodes dans l'objet au travers d'un décorateur.
def decorator(self: object):
    def wrapper(function: Callable):
        setattr(self, function.__name__, MethodType(function, self))
        return function
    return wrapper

# Fonction permettant de créer les objets.
def proto(name: str, methods: dict[str, Callable] = {}) -> type:
    return type(name, (object,), {"__init__": init, "__call__": decorator, **methods})
