from django.contrib import admin
from .models import Place, Image
from django.utils.html import format_html
from adminsortable2.admin import SortableAdminBase, SortableStackedInline


class ImageStackedInline(SortableStackedInline):
    model = Image
    extra = 1
    fields = (('location', 'image'), 'image_preview', 'img_id', 'img_description')
    readonly_fields = ['image_preview']

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{url}" style="max-width: {max_width}px; max-height: {max_height}px; width: auto; height: auto;"/>',
                max_width = 200,
                max_height = 200,
                url=obj.image.url,
            )
        return "No Image"

    image_preview.short_description = "Превью изображения"


@admin.register(Place)
class PlaceAdmin(SortableAdminBase, admin.ModelAdmin):
    list_display = ['place_name', 'place_id']
    search_fields = ['place_name', 'place_id']
    inlines = [ImageStackedInline]
