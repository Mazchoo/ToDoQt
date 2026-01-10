""" "Magic" class that initialises callable members as it's fields"""

from types import LambdaType


class QtStaticModel:
    """Initilise all members that are callable"""

    def __init__(self):
        for var_name, cls in vars(self.__class__).items():
            if isinstance(cls, type) or (
                isinstance(cls, LambdaType) and cls.__name__ == "<lambda>"
            ):
                self.__setattr__(var_name, cls())
