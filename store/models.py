print("MODELS LOADED ✅")

from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg


class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Artist(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField(blank=True, null=True)
    genres = models.ManyToManyField('Genre') 

    def __str__(self):
        return self.name


class Vinyl(models.Model):
    title = models.CharField(max_length=200)
    artist = models.CharField(max_length=100, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    release_year = models.PositiveSmallIntegerField(blank=True, null=True)
    cover_image = models.ImageField(upload_to='vinyl_covers/', blank=True, null=True)
    genres = models.ManyToManyField('Genre', blank=True)
    tracklist = models.TextField(blank=True)

    def __str__(self):
     return f"{self.title} - {self.artist}"



    
    @property
    def avg_rating(self):
        return self.ratings.aggregate(Avg('stars'))['stars__avg'] or 0

   
     
    

class Rating(models.Model):
    vinyl = models.ForeignKey(Vinyl, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)   
    stars = models.PositiveSmallIntegerField()
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.stars} stars for {self.vinyl.title}"
    

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.TextField()
    total_price = models.DecimalField(max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Objednávka #{self.id} – {self.name}"
    

