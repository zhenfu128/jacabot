from django.db import models

class Sensor(models.Model):
    title = models.TextField()
    description = models.TextField(default='null')
    value = models.FloatField()
    time = models.DateTimeField()
