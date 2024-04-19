from django.contrib import admin
from . models import User, Movie_log, Tv_show_log, Movie_review, Tv_review, Genre

# Register your models here.

admin.site.register(User)
admin.site.register(Movie_log)
admin.site.register(Tv_show_log)
admin.site.register(Movie_review)
admin.site.register(Tv_review)
admin.site.register(Genre)
