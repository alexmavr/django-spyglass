from django.conf import settings

def get_meta():
    package = ".".join(settings.METAMODEL.split('.')[:-1])
    modelclass = settings.METAMODEL.split('.')[-1]
    Metamodel = __import__(package, globals(),locals(), [modelclass], -1)
    Metamodel = eval("Metamodel." + modelclass)
    return Metamodel

