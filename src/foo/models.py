from django.db import models

class UserUploadedPhoto(models.Model):
    name = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='user_uploaded_photos')
