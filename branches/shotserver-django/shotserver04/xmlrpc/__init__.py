def signature(*types):
    def decorator(func):
        func._signature = types
        return func
    return decorator
