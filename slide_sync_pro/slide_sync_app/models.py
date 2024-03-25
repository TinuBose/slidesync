from django.db import models

# Create your models here.


class Uploadfile(models.Model):
    upload = models.FileField(upload_to="conversion_model/input", null=False)