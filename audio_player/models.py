from django.db import models

# Create your models here.
class Session(models.Model):
    session_name = models.TextField(verbose_name = "Session Name", unique = True)
    consumer_name = models.TextField(default="")
    media_url = models.URLField(verbose_name="Media URL", null = True)
    metadata = models.TextField(verbose_name="Metadata", default = "")

    def __str__(self):
        return self.session_name