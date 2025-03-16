from django.contrib import admin
from .models import Place, Image

# Register your models here.
@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ['place_name', 'place_id']
    search_fields = ['place_name', 'place_id']
    
@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['location', 'img_id', 'img_description', 'image']
    list_filter = ['location']
    search_fields = ['img_description', 'location']