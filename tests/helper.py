
def show_name(name="Unnamed process"):
    def decorator(function):
        def wrapper(self, *args, **kwargs):
            print("\n-- {} --".format(name))
            function(self, *args, **kwargs)
        return wrapper
    return decorator