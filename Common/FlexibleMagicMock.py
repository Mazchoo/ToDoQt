''' Create a magic mock for mocking widgets and smoke testing functions '''
from unittest.mock import MagicMock


def compareAlwaysTrue(_self, _other):
    ''' Dummy function to do comparisons if called on the magic mock '''
    return True


class FlexibleMagicMock(MagicMock):
    ''' A Magic Mock class that accepts more operations '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.__setattr__('__gt__', compareAlwaysTrue)
        self.__setattr__('__lt__', compareAlwaysTrue)
        self.__setattr__('__ge__', compareAlwaysTrue)
        self.__setattr__('__le__', compareAlwaysTrue)

    def text(self):
        return 'mock text'
