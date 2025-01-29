''' Helper that makes a function a method of a class after the class has been declared '''


class ClassMethod:
    '''
        Decorator class that can add a method to another class e.g.
        @ClassMethod(OtherClass)
        def func(self): print("Hello")

        Will add func to the class OtherClass
    '''
    def __init__(self, cls):
        self.cls = cls

    def __call__(self, func):
        setattr(self.cls, func.__name__, lambda self, *args, **kwargs: func(self, *args, **kwargs))
        return func
