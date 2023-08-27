def with_open_and_close_driver(function):
        def wrapper(*args,**kwargs):
            func = function(*args, **kwargs)
            args[0].driver.close()
            return func
        return wrapper