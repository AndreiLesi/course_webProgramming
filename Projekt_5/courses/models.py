from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.db import models

# Create your models here.
class User(AbstractUser):
    likes = models.ManyToManyField("Course", blank=True, 
            related_name="isLiked")
    enrolled = models.ManyToManyField("Course", blank=True, 
              related_name="students")

    username = models.EmailField(max_length=64, unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=False, null=False)
    last_name = models.CharField(_('last name'), max_length=150, blank=False, null=False)
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self):
        return f"{self.username}"


class Course(models.Model):
    creator = models.ForeignKey(User, related_name="uploadedCourses", 
                on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=10000)
    topics = [
        ("Programming", "Programming"),
        ("Business", "Business"), 
        ("Finance", "Finance"),
        ("Design", "Design"), 
        ("Fotografie", "Fotografie"),
        ("Marketing", "Marketing"),
        ("Music", "Music"),
        ("Health", "Health"),
    ]
    topic = models.CharField(max_length=70, choices=topics)
    price = models.FloatField()
    image = models.URLField(blank=True, default="https://img.icons8.com/ios/" \
                                     "500/000000/no-image.png")
    # ratins = "toAdd"
    def __str__(self):
        return f'{self.title}'

    def serialize(self):
        return {
            "timestamp": self.timestamp,
            "content": self.description
        }


class Comment(models.Model):
    creator = models.ForeignKey(User, related_name="comments", 
              on_delete=models.CASCADE)
    content = models.TextField(max_length=10000)
    course = models.ForeignKey(Course, related_name="comments", 
           on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.creator}'s comment on {self.course}"