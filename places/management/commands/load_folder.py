import json
from pathlib import Path

import requests
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.db import transaction
from django.shortcuts import get_object_or_404

from places.models import Image, Place


class Command(BaseCommand):
    help = "Парсит JSON-файлы из указанной папки и вносит их содержимое в БД"

    def add_arguments(self, parser):
        parser.add_argument(
            "json_folder",
            type=str,
            help="Название папки с json-файлами",
            default="json_data",
        )

    def download_images(self, img_urls, place_pk):
        location = get_object_or_404(
            Place.objects.prefetch_related("images"), pk=place_pk
        )
        last_image = location.images.order_by("-ordinal").first()
        last_number = last_image.ordinal if last_image else 0
        downloaded_images = 0
        updated_images = 0
        for idx, img_url in enumerate(img_urls, start=last_number + 1):
            response = requests.get(img_url, timeout=10)
            img_name = Path(img_url).name
            response.raise_for_status()
            content = ContentFile(response.content, name=img_name)
            image, created = Image.objects.get_or_create(
                location=location,
                ordinal=idx,
                defaults={"description": img_url, "image": content},
            )

            if created:
                downloaded_images += 1
            else:
                updated_images += 1
        if downloaded_images:
            self.stdout.write(
                self.style.SUCCESS(
                    f"{location}: добавлено {downloaded_images} изображений"
                )
            )
        if updated_images:
            self.stdout.write(
                self.style.WARNING(
                    f"{location}: обновлено {updated_images} изображений"
                )
            )

    def check_json(self, json_data):
        required_keys = [
            "title",
            "imgs",
            "coordinates",
            "description_short",
            "description_long",
        ]
        return all(key in json_data for key in required_keys)

    def handle(self, *args, **options):
        try:
            with transaction.atomic():
                json_folder = Path(settings.BASE_DIR / options["json_folder"])
                if not json_folder.exists():
                    raise FileNotFoundError(f"Папка {json_folder} не существует")
                if not json_folder.is_dir():
                    raise NotADirectoryError(f"{json_folder} не является папкой")

                added_locations = 0
                updated_locations = 0

                for json_file in json_folder.glob("*.json"):
                    with open(json_file, "r", encoding="utf-8") as jf:
                        json_data = json.load(jf)
                        if not self.check_json(json_data):
                            raise ValueError("Неверный формат JSON-файла")

                        place_name = json_data.get("title", "")
                        if not place_name:
                            raise ValueError("Отсутствует название локации")

                        coordinates = json_data.get("coordinates", {})
                        if not coordinates:
                            raise ValueError("Отсутствуют координаты")

                        lat, lng = coordinates.get("lat"), coordinates.get("lng")
                        try:
                            float_lat, float_lng = float(lat), float(lng)
                            if abs(float_lat) > 90:
                                raise ValueError(
                                    "Абсолютное значение широты превышает 90 град."
                                )
                            elif abs(float_lng) > 180:
                                raise ValueError(
                                    "Абсолютное значение долготы превышает 180 град."
                                )
                        except ValueError as err:
                            raise err("Координаты заданы некорректно")

                        img_urls = json_data.get("imgs", [])
                        if not img_urls:
                            raise ValueError("Отсутствуют ссылки на изображения")

                        place, created = Place.objects.get_or_create(
                            place_name=place_name,
                            defaults={
                                "latitude": lat,
                                "longitude": lng,
                                "short_description": json_data.get(
                                    "description_short", ""
                                ),
                                "long_description": json_data.get(
                                    "description_long", ""
                                ),
                            },
                        )

                        try:
                            self.download_images(img_urls, place.pk)
                        except Exception as err:
                            self.stdout.write(
                                self.style.ERROR(
                                    f":Ошибка при загрузке изображений для локации {place}"
                                )
                            )
                            raise err

                        if created:
                            self.stdout.write(
                                self.style.SUCCESS(f"Добавлена локация: {place}")
                            )
                            added_locations += 1
                        else:
                            self.stdout.write(
                                self.style.WARNING(f"Обновлена локация: {place}")
                            )
                            updated_locations += 1

            self.stdout.write(
                self.style.SUCCESS(f"Добавлено локаций: {added_locations}")
            )
            self.stdout.write(
                self.style.WARNING(f"Обновлено локаций: {updated_locations}")
            )
        except Exception as err:
            self.stdout.write(self.style.ERROR(f"Ошибка: {str(err)}"))
            raise
