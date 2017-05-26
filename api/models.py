from django.contrib.auth.models import User
from django.db import models


class Notes(models.Model):
    nno=models.IntegerField()
    title=models.TextField(max_length=30)
    text=models.TextField(max_length=500)


