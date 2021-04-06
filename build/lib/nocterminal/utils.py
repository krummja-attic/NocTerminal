from functools import partial, wraps
import logging


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def debug(func=None, *, prefix=''):
    if func is None:
        return partial(debug, prefix=prefix)

    msg = prefix + func.__qualname__

    @wraps(func)
    def wrapper(*args, **kwargs):
        print(msg)
        return func(*args, **kwargs)
    return wrapper


def debugattr(cls):
    orig_getattribute = cls.__getattribute__

    def __getattribute__(self, name):
        print('Get: ', name)
        return orig_getattribute(self, name)
    cls.__getattribute__ = __getattribute__

    return cls


def debugmethod(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return_value = func(*args, **kwargs)
        logger.debug(f'CALL  : {func.__name__}')
        logger.debug(f'WITH  : {args, kwargs}')
        logger.debug(f'RTRN  : {func.__name__} returned {return_value}')
        return return_value
    return wrapper


def debugmethods(cls):
    """Apply debugmethod to all methods of a class."""
    for key, val in vars(cls).items():
        if callable(val):
            setattr(cls, key, debugmethod(val))
    return cls
