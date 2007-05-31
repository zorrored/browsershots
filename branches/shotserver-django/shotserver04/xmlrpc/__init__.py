class ErrorMessage(Exception):

    def __init__(self, message):
        self.message = str(message)


def signature(*types):

    def decorator(func):
        func._signature = types
        return func

    return decorator
