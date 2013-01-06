from django.db import models

class NewsStory(models.Model):
    headline = models.CharField(max_length=200, blank=False)
    category = models.CharField(max_length=200, blank=False)
    subtitle = models.CharField(max_length=200, blank=False)

    def __unicode__(self):
        return self.headline
