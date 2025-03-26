from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class ConfirmationCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)