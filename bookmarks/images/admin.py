from django.contrib import admin
from .models import Image

@admin.register(Image)
class AdminImage(admin.ModelAdmin):
    list_display = ['title', 'slug', 'image', 'created']
    list_filter = ['created']
