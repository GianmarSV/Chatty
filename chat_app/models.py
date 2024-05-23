from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class ChatGroup(models.Model):
    name = models.CharField(max_length=100, unique=True)
    members = models.ManyToManyField(User)

    def __str__(self):
        return self.name


class ChatMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(ChatGroup, on_delete=models.CASCADE)
    message = models.TextField()
    send_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.group_name} - {self.send_date}"
