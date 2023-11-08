from django.db import models
from accounts.models import MyUser

# Create your models here.

class Question(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name="questions")
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class Answer(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name="answered_user")
    question = models.ForeignKey(Question, on_delete= models.CASCADE, related_name="answer")
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.answer

class Like(models.Model):
    answer = models.ForeignKey(Answer, on_delete= models.CASCADE, related_name="likes")
    user = models.ForeignKey(MyUser, on_delete= models.CASCADE, related_name='liked_user')
    