from django.contrib import admin
from tastypie.admin import ApiKeyInline
from tastypie.models import ApiAccess, ApiKey
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from spyglass.models import Site
from spyglass.models import DataField
from spyglass.models import Crawler
from spyglass.models import Query
from spyglass.models import Notification

admin.site.register(Site)
admin.site.register(DataField)
admin.site.register(Crawler)
admin.site.register(Query)
admin.site.register(Notification)

admin.site.register(ApiKey)
admin.site.register(ApiAccess)

class UserModelAdmin(UserAdmin):
    inlines = UserAdmin.inlines + [ApiKeyInline]

admin.site.unregister(User)
admin.site.register(User,UserModelAdmin)
