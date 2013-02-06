from django.conf import settings
SPYGLASS_AUTHORIZED_QUERIES = getattr(settings, 'SPYGLASS_AUTHORIZED_QUERIES', True)
SPYGLASS_ADD_USERS = getattr(settings, 'SPYGLASS_ADD_USERS', False)
