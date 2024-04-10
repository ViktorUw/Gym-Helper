from django.contrib import admin

from .models import Exercises, Category

# Register your models here.

admin.site.register((Exercises, Category))