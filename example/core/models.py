from django.db import models

# The Developer's model. Spyglass will populate it with its results
class NewsStory(models.Model):
    headline = models.CharField(max_length=200, blank=False)
    category = models.CharField(max_length=200, blank=False)
    subtitle = models.CharField(max_length=200, blank=False)

    def __unicode__(self):
        return self.headline

    class Meta:
        verbose_name_plural = "newsstories"
