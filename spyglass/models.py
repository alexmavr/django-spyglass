from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from tastypie.models import create_api_key

# Auto generate Api Key on user creation
models.signals.post_save.connect(create_api_key, sender=User)

# note: Site.datafields.all() should work

class Site(models.Model):
    name = models.CharField(max_length=150, blank=False, verbose_name="Site Name")
    url = models.URLField(max_length=400, blank=False, verbose_name="Site URL")

    def __unicode__(self):
        return self.name

class DataField(models.Model):
    site = models.ForeignKey(Site, verbose_name="Site", related_name="datafields")
    field_name = models.CharField(max_length=150, blank=False, verbose_name="Field Name")
        # Add support for different parsers? (beautiful soup pl0x)
    xpath = models.CharField(max_length=150, blank=False, verbose_name="XPath")

    def __unicode__(self):
        return self.site.name


class Query(models.Model):
    email = models.EmailField(blank=False, verbose_name="User Email")
    site = models.ForeignKey(Site, verbose_name="Site")
    completed = models.BooleanField(default=False, blank=False, verbose_name="Completed")
    metamodel = models.OnetoOneField(settings.metamodel, verbose_name="Meta Model")

    def __unicode__(self):
        return self.email


class Crawler(models.Model):
    api_key = models.CharField(max_length=100, primary_key=True, verbose_name="Crawler Api Key")
    last_seen = models.DateTimeField(auto_now=True, auto_now_add=True, verbose_name="Last Seen At")
    trust_level = models.IntegerField(default=10, blank=False, verbose_name="Trust Level")

    def __unicode__(self):
        return self.api_key
