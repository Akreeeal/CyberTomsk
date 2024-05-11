from django.contrib import admin
from .models import Computer, Reservation, Review

admin.site.register(Computer)
admin.site.register(Reservation)
admin.site.register(Review)