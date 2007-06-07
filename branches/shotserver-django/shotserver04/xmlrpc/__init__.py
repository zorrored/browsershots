def register(*signature):

    def wrapper(func):
        func._signature = signature
        return func

    return wrapper
