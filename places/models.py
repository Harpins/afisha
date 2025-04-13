from django.db import models
from django.urls import reverse
from tinymce.models import HTMLField


class Place(models.Model):
    """Модель для хранения локаций"""

    place_name = models.CharField(max_length=255, verbose_name="Название локации")
    latitude = models.DecimalField(
        verbose_name="Широта", decimal_places=14, max_digits=17
    )
    longtitude = models.DecimalField(
        verbose_name="Долгота", decimal_places=14, max_digits=18
    )
    short_description = HTMLField(verbose_name="Короткое описание", blank=True)
    long_description = HTMLField(verbose_name="Длинное описание", blank=True)

    class Meta:
        ordering = ["place_name"]

    def __str__(self):
        return self.place_name

    def get_absolute_url(self):
        return reverse("place_name", kwargs={"pk": self.pk})

    def get_features(self):
        return {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [float(self.longtitude), float(self.latitude)],
            },
            "properties": {
                "title": self.place_name,
                "placeId": self.pk,
                "detailsUrl": self.get_absolute_url(),
            },
        }


class Image(models.Model):
    """Модель для хранения изображений"""

    image = models.ImageField(
        verbose_name="Изображение", upload_to="images/", default=None
    )
    location = models.ForeignKey(
        Place,
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name="Локация",
        null=True,
        blank=True,
    )
    ordinal = models.PositiveIntegerField(
        verbose_name="Порядковый номер", db_index=True, default=1
    )
    description = models.CharField(
        max_length=255, verbose_name="Описание изображения", blank=True
    )

    class Meta:
        ordering = ["ordinal", "location__place_name"]
        unique_together = ["location", "ordinal"]

    def __str__(self):
        return f"{self.pk} {self.location}"
