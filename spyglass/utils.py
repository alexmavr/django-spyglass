from django.conf import settings
from .app_settings import authorized

# Usage: @conditional_decorator(decorator, condition)
# Condition is a string to be evaluated at each call
class authorization_decorator(object):
    def __init__(self, dec):
        self.decorator = dec

    def __call__(self, func):
        if authorized:
            return self.decorator(func)
        else:
            return func

# Receive the metamodel class from settings.METAMODEL
def get_meta():
    package = ".".join(settings.METAMODEL.split('.')[:-1])
    modelclass = settings.METAMODEL.split('.')[-1]
    Metamodel = __import__(package, globals(),locals(), [modelclass], -1)
    Metamodel = eval("Metamodel." + modelclass)
    return Metamodel

