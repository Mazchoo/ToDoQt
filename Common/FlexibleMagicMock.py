from unittest.mock import MagicMock


def compareAlwaysTrue(_self, _other):
    return True


class FlexibleMagicMock(MagicMock):
    ''' A Magic Mock class that allows comparison. '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.__setattr__('__gt__', compareAlwaysTrue)
        self.__setattr__('__lt__', compareAlwaysTrue)
        self.__setattr__('__ge__', compareAlwaysTrue)
        self.__setattr__('__le__', compareAlwaysTrue)


    def text(self):
        return 'mock text'