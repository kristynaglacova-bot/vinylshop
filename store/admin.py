from django.contrib import admin
from .models import Vinyl, Rating, Genre, Artist, Order

admin.site.register(Vinyl)
admin.site.register(Rating)
admin.site.register(Artist)
admin.site.register(Genre)
admin.site.register(Order)