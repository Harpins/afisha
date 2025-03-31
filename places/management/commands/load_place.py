from django.core.management.base import BaseCommand
import json
from django.db import transaction
from django.core.files.base import ContentFile
from pathlib import Path
from django.conf import settings
from places.models import Place, Image
import requests
import re
from transliterate import translit
from django.shortcuts import get_object_or_404


class Command(BaseCommand):
    help = "Парсит JSON-файлы из указанной папки и вносит их содержимое в БД"

    def add_arguments(self, parser):
        parser.add_argument(
            "--json_folder",
            type=str,
            help="Название папки с json-файлами",
            default="json_data",
        )
        
    def download_images(self, img_urls, place_id):
        location = get_object_or_404(Place, place_id=place_id)
        downloaded_images = []
        updated_images = []
        for idx, img_url in enumerate(img_urls, start=1):
            response = requests.get(img_url, timeout=10)
            img_name = Path(img_url).name
            response.raise_for_status()
            content = ContentFile(response.content, name=img_name)
            image, created = Image.objects.get_or_create(
                location=location,
                img_id=idx,
                defaults={"description": img_url, "image": content},
            )
            
            if created:
                downloaded_images.append(img_name)
            else:
                updated_images.append(img_name)
        if downloaded_images:        
            self.stdout.write(self.style.SUCCESS(f"{location}: добавлено {len(downloaded_images)} изображений"))
        if updated_images:
            self.stdout.write(self.style.WARNING(f"{location}: обновлено {len(updated_images)} изображений")) 

    def get_place_id(self, place_name):
        cleaned_id = re.sub(r"[^a-zA-Zа-яА-Я0-9]", "", place_name)
        return translit(cleaned_id, "ru", reversed=True)

    def handle(self, *args, **options):
        try:
            with transaction.atomic():
                json_folder = Path(settings.BASE_DIR / options["json_folder"])
                if not (json_folder.exists() and json_folder.is_dir()):
                    self.stdout.write(
                        self.style.ERROR(f"Папка {json_folder} не обнаружена")
                    )
                    raise FileNotFoundError(f"Папка {json_folder} не обнаружена")

                for json_file in json_folder.glob("*.json"):
                    with open(json_file, "r", encoding="utf-8") as jf:
                        json_data = json.load(jf)
                        place_name = json_data.get("title", "noname")
                        place_id = self.get_place_id(place_name)
                        coordinates = json_data.get("coordinates", {})
                        description_short = json_data.get("description_short", "")
                        description_long = json_data.get("description_short", "")
                        img_urls = json_data.get("imgs", [])
                        location, created = Place.objects.get_or_create(
                            place_id=place_id,
                            defaults={
                                "place_name": place_name,
                                "latitude": coordinates.get("lat", "50"),
                                "longtitude": coordinates.get("lng", "30"),
                                "description_short": description_short,
                                "description_long": description_long,
                            },
                        )
                        self.download_images(img_urls, place_id)
                        if created:
                            self.stdout.write(
                                self.style.SUCCESS(f"Добавлена локация: {location}")
                            )
                        else:
                            self.stdout.write(
                                self.style.WARNING(f"Обновлена локация: {location}")
                            )

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Ошибка: {str(e)}"))
            raise
