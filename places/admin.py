from adminsortable2.admin import SortableAdminBase, SortableStackedInline
from django.contrib import admin
from django.utils.html import format_html

from .models import Image, Place


class ImageStackedInline(SortableStackedInline):
    model = Image
    extra = 1
    fields = (("location", "image"), "image_preview", "ordinal", "description")
    readonly_fields = ["image_preview"]

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{url}" '
                'style="max-width: {max_width}px; max-height: {max_height}px;"'
                'width="auto" height="auto"/>',
                max_width=200,
                max_height=200,
                url=obj.image.url,
            )
        return "No Image"

    image_preview.short_description = "Превью изображения"


@admin.register(Place)
class PlaceAdmin(SortableAdminBase, admin.ModelAdmin):
    list_per_page = 50
    list_display = ["place_name", "pk"]
    search_fields = ["place_name", "pk"]
    inlines = [ImageStackedInline]


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_per_page = 50
    list_select_related = ["location"]
    search_fields = ["location__place_name", "ordinal"]
    autocomplete_fields = ["location"]
    ordering = ["location__place_name", "ordinal"]
    list_display = ["image_preview", "location", "ordinal"]
    readonly_fields = ["image_preview"]

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{url}" '
                'style="max-width: {max_width}px; max-height: {max_height}px;"'
                'width="auto" height="auto"/>',
                max_width=100,
                max_height=100,
                url=obj.image.url,
            )
        return "No Image"

    image_preview.short_description = "Превью изображения"
