from pathlib import Path
from urllib.parse import urljoin

import requests
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction
from environs import Env

env = Env()
env.read_env()


class Command(BaseCommand):
    help = "Скачивает json-файлы по ссылке на репозиторий"

    def add_arguments(self, parser):
        parser.add_argument(
            "folder",
            type=str,
            help="Путь к папке, в которую будут загружены JSON-файлы",
            default="json_data",
        )

    def handle(self, *args, **options):
        try:
            with transaction.atomic():
                repo_id = env("REPO_ID")
                json_dir = env("JSON_DIR")
                api_url = f"https://api.github.com/repos/{repo_id}/contents/{json_dir}"
                raw_url = f"https://raw.githubusercontent.com/{repo_id}/master/"
                json_folder = Path(settings.BASE_DIR / options["folder"])
                json_folder.mkdir(parents=True, exist_ok=True)

                response = requests.get(api_url, timeout=10)
                response.raise_for_status()
                json_files = [
                    jf["name"] for jf in response.json() if jf["name"].endswith(".json")
                ]
                if json_files:
                    self.stdout.write(
                        self.style.SUCCESS(f"Найдено {len(json_files)} JSON-файлов")
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(
                            f"JSON-файлы не найдены в директории {json_dir} репозитория {repo_id}"
                        )
                    )
                    return

                for json_file in json_files:
                    file_url = urljoin(raw_url, f"{json_dir}/{json_file}")
                    response = requests.get(file_url, timeout=10)
                    response.raise_for_status()
                    with open(json_folder / json_file, "wb") as jf:
                        jf.write(response.content)

                self.stdout.write(self.style.SUCCESS(f"Загрузка JSON завершена"))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Ошибка: {str(e)}"))
            raise
