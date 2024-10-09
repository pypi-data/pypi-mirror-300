from typing import Callable
from types import MethodType
from copy import deepcopy

# Fonction permettant de servir d'initiateur aux objets.
def init(self, *args, **kwargs) -> None:
    for index, arg in enumerate(args):
        setattr(self, "arg%s" % index, arg)
    for key, value in kwargs.items():
        setattr(self, key, value)
    return

# Fonction gérant l'entrée du with.
def wEnter(self):
    return self

# Fonction gérant la sortie du with.
def wExit(self, executionType, executionValue, traceback):
    return self

# Fonction gérant les appels de l'objet.
def decorator(self, *args, **kwargs):
    if hasattr(args[0], "__call__"):
        setattr(self, args[0].__name__, MethodType(args[0], self))
    else:
        o = deepcopy(self)
        o.new(*args, **kwargs)
        return o
    return self

# Fonction permettant de créer les objets.
def proto(name: str, methods: dict[str, Callable] = {}) -> type:
    o = type(name, (object,), {
        "__init__": init,
        "__call__": decorator,
        "__enter__": wEnter,
        "__exit__": wExit,
        **methods
    })
    return o()