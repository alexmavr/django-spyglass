from django.contrib import admin
from spyglass.models import Site
from spyglass.models import DataField
from spyglass.models import Crawler
from spyglass.models import Query

admin.site.register(Site)
admin.site.register(DataField)
admin.site.register(Crawler)
admin.site.register(Query)
