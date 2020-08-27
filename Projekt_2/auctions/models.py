from django.contrib.auth.models import AbstractUser
from django.db import models


class Listing(models.Model):
    createdBy = models.ForeignKey("User", related_name="listings", 
                                  on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    description = models.TextField(max_length=10000)
    startingPrice = models.FloatField()
    imageURL = models.URLField(blank=True)
    categories = [
        ("Books", "Books"),
        ("Technology", "Technology"), 
        ("Home", "Home"),
        ("Sports & Outdoors", "Sports & Outdoors"), 
        ("Beauty & Personal Care", "Beauty & Personal Care"),
        ("Fashion", "Fashion"),
        ("Other", "Other")]
    category = models.CharField(max_length=64, choices=categories)
    currentPrice = models.FloatField(blank=True, null=True)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} by {self.createdBy}"


class User(AbstractUser):
    watchlist = models.ManyToManyField(Listing, blank=True, 
                                        related_name="watchers")

    def __str__(self):
        return f"{self.username}"


class Bid(models.Model):
    createdBy = models.ForeignKey("User", related_name="bids", 
                                  on_delete=models.CASCADE)
    listing = models.ForeignKey("Listing", related_name="bids", 
                                on_delete=models.CASCADE)
    bidPrice = models.IntegerField()

    def __str__(self):
        return f"({self.id}) {self.createdBy} bid {self.bidPrice} for {self.listing}"


class Comment(models.Model):
    createdBy = models.ForeignKey("User", related_name="comments", 
                                  on_delete=models.CASCADE )
    listing = models.ForeignKey("Listing", related_name="comments", 
                                on_delete=models.CASCADE)
    description = models.TextField(max_length=1000)
    createdAt = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"({self.id}) {self.createdBy}'s comment on {self.listing}"