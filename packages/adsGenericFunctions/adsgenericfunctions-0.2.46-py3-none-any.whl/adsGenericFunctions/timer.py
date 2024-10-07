import timeit
from .global_config import get_timer

def timer(func):
    """ Décorateur pour mesurer le temps d'exécution d'une fonction si le timer est activé """
    def wrapper(self, *args, **kwargs):
        if get_timer():
            start_time = timeit.default_timer()
            result = func(self, *args, **kwargs)
            elapsed_time = timeit.default_timer() - start_time
            self.logger.info(f"Temps d'exécution de {func.__name__}: {elapsed_time:.4f} secondes")
            return result
        else:
            return func(self, *args, **kwargs)

    return wrapper

"""
def timer_class(cls):
    my_package = None
    for attr_name, attr_value in cls.__dict__.items():
        print(attr_value)
        if isinstance(attr_value, Logger):
            my_package = attr_value
            break
    if not my_package:
        raise ValueError("Le my_package n'a pas été trouvé dans la classe.")
    for attr_name, attr_value in cls.__dict__.items():
        if callable(attr_value):
            if not (attr_name.startswith('__') and attr_name.endswith('__')) and not attr_name.startswith(f"_{cls.__name__}__") and attr_name != 'read':
                setattr(cls, attr_name, timer(my_package)(attr_value))
    return cls
"""