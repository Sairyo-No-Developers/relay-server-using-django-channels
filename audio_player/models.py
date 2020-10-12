from django.db import models

# Create your models here.
class Session(models.Model):
    session_name = models.TextField(verbose_name = "Session Name", unique = True)
    consumer_name = models.TextField(default="")

    def __str__(self):
        return self.session_name