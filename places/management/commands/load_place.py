from pathlib import Path

import requests
from urllib.parse import urlparse
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.db import transaction

from places.models import Image, Place


class Command(BaseCommand):
    help = "Парсит JSON-файл по ссылке и вносит его содержимое в БД"

    def add_arguments(self, parser):
        parser.add_argument("json_url", type=str, help="Ссылка на JSON-файл")

    def download_images(self, img_urls, place):
        last_image = place.images.order_by("-ordinal").first()
        last_number = last_image.ordinal if last_image else 0
        downloaded_images = 0
        updated_images = 0
        for idx, img_url in enumerate(img_urls, start=last_number + 1):
            response = requests.get(img_url, timeout=10)
            img_name = Path(img_url).name
            response.raise_for_status()
            content = ContentFile(response.content, name=img_name)
            image, created = Image.objects.get_or_create(
                location=place,
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
                    f"{place}: добавлено {downloaded_images} изображений"
                )
            )
        if updated_images:
            self.stdout.write(
                self.style.WARNING(f"{place}: обновлено {updated_images} изображений")
            )

    def check_json(self, json_data):
        required_keys = [
            "title",
            "imgs",
            "coordinates",
        ]
        return all(key in json_data for key in required_keys)

    def handle(self, *args, **options):
        try:
            with transaction.atomic():
                url = options["json_url"]
                parsed_url = urlparse(url)
                if not parsed_url.scheme:
                    url = f"https://{url}"
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                try:
                    place_raw = response.json()
                    if not self.check_json(place_raw):
                        raise ValueError("Неверный формат JSON-файла")
                except requests.exceptions.JSONDecodeError:
                    self.stdout.write(
                        self.style.ERROR_OUTPUT("Сервер возвращает не JSON")
                    )
                    raise

                place_name = place_raw.get("title", "")
                if not place_name:
                    raise ValueError("Отсутствует название локации")

                coordinates = place_raw.get("coordinates", {})
                if not coordinates:
                    raise ValueError("Отсутствуют координаты")

                lat, lng = coordinates.get("lat"), coordinates.get("lng")

                try:
                    float_lat, float_lng = float(lat), float(lng)
                    if abs(float_lat) > 90:
                        raise ValueError(
                            "Абсолютное значение широты превышает 90 град."
                        )
                    if abs(float_lng) > 180:
                        raise ValueError(
                            "Абсолютное значение долготы превышает 180 град."
                        )
                except (TypeError, ValueError) as err:
                    raise ValueError("Координаты заданы некорректно") from err

                img_urls = place_raw.get("imgs", [])
                if not img_urls:
                    raise ValueError("Отсутствуют ссылки на изображения")

                place, created = Place.objects.get_or_create(
                    place_name=place_name,
                    defaults={
                        "latitude": lat,
                        "longitude": lng,
                        "short_description": place_raw.get("description_short", ""),
                        "long_description": place_raw.get("description_long", ""),
                    },
                )

                try:
                    self.download_images(img_urls, place)
                except Exception as err:
                    self.stdout.write(
                        self.style.ERROR(
                            f":Ошибка при загрузке изображений для локации {place}"
                        )
                    )
                    raise err

                if created:
                    self.stdout.write(self.style.SUCCESS(f"Добавлена локация: {place}"))
                else:
                    self.stdout.write(self.style.WARNING(f"Обновлена локация: {place}"))

        except Exception as err:
            self.stdout.write(self.style.ERROR(f"Ошибка: {str(err)}"))
            raise
