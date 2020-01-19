class SchemaError(TypeError):
    pass


class ValidationError(ValueError):

    def __init__(self, *, data):
        self.data = data
        super().__init__(data)
