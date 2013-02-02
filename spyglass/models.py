from datetime import timedelta
from django.utils.timezone import now
from django.db import models
from django.contrib.auth.models import User
from tastypie.models import create_api_key
from .common import get_meta

# Auto generate Api Key on user creation
models.signals.post_save.connect(create_api_key, sender=User)

# The developer class to be populated by spyglass
Metamodel = get_meta()

class Site(models.Model):
    name = models.CharField(max_length=150, blank=False,
                                    verbose_name="Site Name")
    url = models.URLField(max_length=400, blank=False, verbose_name="Site URL")
    poll_time = models.IntegerField(blank=False,
                                    verbose_name="Polling time in minutes")

    def __unicode__(self):
        return self.name

class DataField(models.Model):
    site = models.ForeignKey(Site, verbose_name="Site",
                                 related_name="datafields_set")
    field_name = models.CharField(max_length=150, blank=False,
                                  verbose_name="Field Name")
    xpath = models.CharField(max_length=150, blank=False, verbose_name="XPath")

    def __unicode__(self):
        return self.field_name + " for " + self.site.name


class Query(models.Model):
    user = models.ForeignKey(User)
    site = models.ForeignKey(Site, verbose_name="Site")
    result = models.ForeignKey(Metamodel, blank=True, null=True, default=None)
    completed = models.BooleanField(default=False, blank=False,
                                    verbose_name="Completed")
    persistent = models.BooleanField(default=False, blank=False,
                                    verbose_name="Persistent")
    params = models.CharField(max_length=200, blank=False,
                                    verbose_name="Query Parameters")
    next_check = models.DateTimeField(auto_now_add=True, verbose_name="Next check")
    last_mod = models.DateTimeField(blank=True, verbose_name="Last Modified")

    def save(self, *args, **kwargs):
        self.next_check = now() + timedelta(
                    minutes=self.site.poll_time)
        super(Query, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.params + " at " + self.site.name + " for " + self.user.email


class Crawler(models.Model):
    api_key = models.CharField(max_length=100, primary_key=True,
                                   verbose_name="Crawler Api Key")
    last_seen = models.DateTimeField(auto_now=True, auto_now_add=True,
                                     verbose_name="Last Seen At")
    trust_level = models.IntegerField(default=10, blank=False,
                                      verbose_name="Trust Level")

    def __unicode__(self):
        return self.api_key
