from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
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
    title = models.CharField(max_length=60)
    description = models.TextField(max_length=10000)
    outline = models.TextField(max_length=10000)
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
    length = models.IntegerField()
    effortLevels = [
        ("0–6 hours per week", "0–6 hours per week"),
        ("7–18 hours per week", "7–18 hours per week"),
        ("19–30 hours per week", "19–30 hours per week"),
    ]
    effort = models.CharField(max_length=100, choices=effortLevels)
    levels = [
        ("Introductory", "Introductory"),
        ("Intermediate", "Intermediate"),
        ("Advanced", "Advanced"),
    ]
    level = models.CharField(max_length=100, choices=levels)
    language = models.CharField(max_length=100)
    types = [
        ("Self-paced on your time", "Self-paced on your time"),
        ("Instructor-led schedule", "Instructor-led schedule")
    ]
    type = models.CharField(max_length=150, choices=types)
    price = models.FloatField()
    image = models.URLField(blank=True, default="https://images.unsplash.com/" \
                        "photo-1498243691581-b145c3f54a5a?fit=crop&w=500&q=60")
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


class Rating(models.Model):
    creator = models.ForeignKey(User, related_name="ratings", 
              on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    course = models.ForeignKey(Course, related_name="ratings", 
           on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.creator}: {self.rating}"