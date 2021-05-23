from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Essay(models.Model):
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    # on_delete=models.CASCADE : 계정이 삭제되면 계정과 연결된 Question 모델 데이터를 모두 삭제하는 의미
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.TextField(blank=True)
    like_users = models.ManyToManyField(User, related_name="like_posts", blank=True)

    def __str__(self):
        return self.subject

class Answer(models.Model):
    essay = models.ForeignKey(Essay, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # like_users = models.ManyToManyField(User, related_name="like_answer", blank=True)
    

    