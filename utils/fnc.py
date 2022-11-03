class Maybe(object):
    def __init__(self, value):
        self.value = value

    @classmethod
    def unit(cls, value):
        return cls(value)

    def bind(self, f):
        if self.value is None:
            return self

        result = f(self.value)
        if isinstance(result, Maybe):
            return result
        else:
            return Maybe.unit(result)

    def __getattr__(self, name):
        field = getattr(self.value, name)
        if not callable(field):
            return self.bind(lambda _: field)
        return lambda *args, **kwargs: self.bind(lambda _: field(*args, **kwargs))
