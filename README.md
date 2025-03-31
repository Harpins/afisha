# Сайт c интерактивной картой
[Ссылка на сайт](https://harpins.pythonanywhere.com/)

Пример сайта с интерактивной картой 

## Запуск

Для запуска сайта вам понадобится Python версии 3.10.0

- Скачайте код
- Установите зависимости командой `pip install -r requirements.txt`
- Создайте файл базы данных и сразу примените все миграции командой `python manage.py migrate`
- Настройте учетную запись администратора командой `python manage.py createsuperuser`
- Запустите сервер командой `python manage.py runserver`

## Добавление новых локаций

Для добавления новых локаций зайдите в админку Django.

Добавление новых локаций происходит в списке `Places`.
В админке доступны следующие поля:
- Название локации: текст (обязательное, до 255 знаков)
- ID локации: текст (обязательное и уникальное до 255 знаков)
- Широта: десятичная дробь, до 14 знаков после запятой (дефолтное значение -90.0)
- Долгота: десятичная дробь, до 14 знаков после запятой (дефолтное значение -180.0)
- Короткое описание: текст до 300 знаков
- Длинное описание: текст с поддержкой WYSIWYG-редактора `django-tinymce` (до 5000 знаков)
В `Places` доступен поиск по названию локации и ее ID

К каждой локации можно привязать изображения.
Список изображений представлен в виде сортируемой Inline-таблицы для `Places`.
В админке доступны следующие поля:
- ID изображения (создается автоматически)
- Ссылка на изображение
- Превью изображения (создается автоматически после сохранения изображения)
- Описание изображения: текст до 100 знаков


## Пользовательские команды

Для автоматического заполнения БД реализованы следующие команды:

`python manage.py load_json`
Загружает набор json файлов из репозитория на GitHub.

Аргументы:
- "--json_data" : Путь к папке, в которую будут загружены json-файлы, default="json_data"

**Важно** - Перед запуском команды обязательно задайте переменные окружения `REPO_ID` и `JSON_DIR`

С примерами JSON-файлов можно ознакомиться по [ссылке](https://github.com/devmanorg/where-to-go-places/tree/master/places)

`python manage.py load_place`
Парсит загруженные json-файлы и заполняет БД на их основе.
Аргументы:
- "--json_data" : Путь к папке, в которую загружены json-файлы, default="json_data"


## Переменные окружения

Часть настроек проекта берётся из переменных окружения. Чтобы их определить, создайте файл `.env` рядом с `manage.py` и запишите туда данные в таком формате: `ПЕРЕМЕННАЯ=значение`.

Доступны 5 переменных:
- `DEBUG` — дебаг-режим. Поставьте True, чтобы увидеть отладочную информацию в случае ошибки.
- `SECRET_KEY` — секретный ключ проекта
- `ALLOWED_HOSTS` — см [документацию Django](https://docs.djangoproject.com/en/3.1/ref/settings/#allowed-hosts).
- `REPO_ID` — ссылка на репозиторий в формате `github_account/repository_name`
- `JSON_DIR` — путь к директории с json-файлами для наполнения БД


## Цели проекта

Код написан в учебных целях — это урок в курсе по Python и веб-разработке на сайте [Devman](https://dvmn.org).
