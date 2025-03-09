from django.contrib import admin
from .models import Place, Image

# Register your models here.
@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ['place_name']
    
@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['image_str', 'img_description', 'image']
    list_filter = ['location__place_name']
    search_fields = ['img_description', 'location__place_name']
    
    def image_str(self, obj):
        return str(obj)
    image_str.short_description = 'Изображение'