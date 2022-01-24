from functools import wraps

def client_only(function):

    @wraps(function)
    def wrapper(*args, **kwargs):
        if args[-1] == "client":
            return function(*args, **kwargs)
        errmsg = f"Server {args[-2].getpeername()[0]} attempt access to client function!"
        args[-3].error(errmsg)
        return errmsg

    return wrapper


def server_only(function):

    @wraps(function)
    def wrapper(*args, **kwargs):
        if args[-1] == "server":
            return function(*args, **kwargs)
        errmsg = f"Client {args[-2].getpeername()[0]} attempt access to client function!"
        args[-3].error(errmsg)
        return errmsg

    return wrapper
