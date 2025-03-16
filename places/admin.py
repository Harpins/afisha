from django.contrib import admin
from .models import Place, Image

class ImageInline(admin.TabularInline):
    model = Image
    extra = 1
    
    
@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ['place_name', 'place_id']
    search_fields = ['place_name', 'place_id']
    inlines = [ImageInline]
    
