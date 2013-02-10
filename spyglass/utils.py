from django.conf import settings

# Usage: @conditional_decorator(decorator, condition)
class conditional_decorator(object):
    def __init__(self, dec, condition):
        self.decorator = dec
        self.condition = condition

    def __call__(self, func):
        if not self.condition:
            return func
        return self.decorator(func)

# Receive the metamodel class from settings.METAMODEL
def get_meta():
    package = ".".join(settings.METAMODEL.split('.')[:-1])
    modelclass = settings.METAMODEL.split('.')[-1]
    Metamodel = __import__(package, globals(),locals(), [modelclass], -1)
    Metamodel = eval("Metamodel." + modelclass)
    return Metamodel

