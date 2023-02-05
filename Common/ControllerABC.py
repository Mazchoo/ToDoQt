from abc import ABCMeta
from abc import abstractmethod
from inspect import signature, getattr_static


class ControllerABC(metaclass=ABCMeta):
    '''
        A Controller object has to adhere to the functions defined in this class.
        These functions must all be static methods and have one input argument.
    '''

    @abstractmethod
    def setupCallbacks(self):
        raise NotImplementedError

    @abstractmethod
    def initializeModels(self):
        raise NotImplementedError

    @abstractmethod
    def initializeUi(self):
        raise NotImplementedError

    @classmethod
    def __subclasshook__(cls, sub):
        if not hasattr(sub, 'setupCallbacks'):
            return False
        elif not isinstance(getattr_static(sub, "setupCallbacks"), staticmethod):
            return False
        elif len(signature(sub.setupCallbacks).parameters) != 1:
            return False
        elif not hasattr(sub, 'initializeModels'):
            return False
        elif not isinstance(getattr_static(sub, "initializeModels"), staticmethod):
            return False
        elif len(signature(sub.initializeModels).parameters) != 1:
            return False
        elif not hasattr(sub, 'initializeUi'):
            return False
        elif not isinstance(getattr_static(sub, "initializeUi"), staticmethod):
            return False
        elif len(signature(sub.initializeUi).parameters) != 1:
            return False
        else:
            return True
