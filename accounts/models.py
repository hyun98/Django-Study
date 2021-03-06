from django.db import models
from django.conf import settings

class Profile(models.Model):
    # User모델과 Profile을 1:1로 연결
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    nickname = models.CharField(max_length=40, blank=True)
    image = models.ImageField(blank=True)
    followings = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="followers")