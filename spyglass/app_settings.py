from django.conf import settings

def authorized():
    return getattr(settings, 'SPYGLASS_AUTHORIZED_QUERIES', True)

def add_users():
    return getattr(settings, 'SPYGLASS_ADD_USERS', False)
