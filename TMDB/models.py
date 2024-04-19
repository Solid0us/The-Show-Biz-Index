from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

class User(AbstractUser):
    pass

class Genre(models.Model):
    genre = models.CharField(max_length=100, primary_key=True)
    id = models.IntegerField()

class Movie_log(models.Model):
    movie_id = models.IntegerField(blank=False, primary_key=True)
    movie_name = models.CharField(max_length=255, blank=False)
    planned_watcher = models.ManyToManyField(User, related_name="planned_movie_watcher", blank=True)
    movie_watcher = models.ManyToManyField(User, related_name="user_movie_watcher", blank=True)
    finished_watcher = models.ManyToManyField(User, related_name="movie_watcher_finished", blank=True)
    movie_genre = models.ManyToManyField(Genre, related_name="genre_movie")
    backdrop_url = models.URLField(blank=True, null=True)

class Tv_show_log(models.Model):
    tv_id = models.IntegerField(blank=False, primary_key=True)
    tv_name = models.CharField(max_length=255, blank=False)
    planned_watcher = models.ManyToManyField(User, related_name="planned_tv_watcher", blank=True)
    tv_watcher = models.ManyToManyField(User, related_name="user_tv_watcher", blank=True)
    finished_watcher = models.ManyToManyField(User, related_name="tv_watcher_finished", blank=True)
    tv_genre = models.ManyToManyField(Genre, related_name="genre_tv")
    backdrop_url = models.URLField(blank=True, null=True)

class Movie_review(models.Model):
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    movie_id = models.ForeignKey(Movie_log, on_delete=models.CASCADE, related_name="movie_review")
    review = models.TextField(blank = True, max_length=1000)
    score = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    review_date = models.DateTimeField(auto_now=True)

class Tv_review(models.Model):
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    tv_id = models.ForeignKey(Tv_show_log, on_delete=models.CASCADE , related_name="tv_review")
    review = models.TextField(blank = True, max_length=1000)
    score = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    review_date = models.DateTimeField(auto_now=True)



