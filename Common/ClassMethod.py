
class ClassMethod:
    def __init__(self, cls):
        self.cls = cls

    def __call__(self, func):
        setattr(self.cls, func.__name__, func)
        return func
