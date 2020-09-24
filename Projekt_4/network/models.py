from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    likes = models.ManyToManyField("Post", blank=True, 
            related_name="likes")
    follows = models.ManyToManyField("self", blank=True, symmetrical=False, 
              related_name="followers", default=0)

    def __str__(self):
        return f"{self.username}"


class Post(models.Model):
    creator = models.ForeignKey(User, related_name="posts", 
                on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField(max_length=10000)

    def __str__(self):
        return f'{self.creator} from {self.timestamp.strftime("%d.%m.%Y %H:%M")}'

    def serialize(self):
        return {
            "timestamp": self.timestamp,
            "content": self.content
        }


class Comment(models.Model):
    creator = models.ForeignKey(User, related_name="comments", 
              on_delete=models.CASCADE)
    content = models.TextField(max_length=10000)
    post = models.ForeignKey(Post, related_name="comments", 
           on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.creator}'s comment on {self.post}"