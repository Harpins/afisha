# Generated by Django 5.1.7 on 2025-04-13 21:33

import django.db.models.deletion
import tinymce.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('place_name', models.CharField(max_length=255, verbose_name='Название локации')),
                ('latitude', models.DecimalField(decimal_places=14, max_digits=17, unique=True, verbose_name='Широта')),
                ('longtitude', models.DecimalField(decimal_places=14, max_digits=18, unique=True, verbose_name='Долгота')),
                ('short_description', tinymce.models.HTMLField(blank=True, verbose_name='Короткое описание')),
                ('long_description', tinymce.models.HTMLField(blank=True, verbose_name='Длинное описание')),
            ],
            options={
                'ordering': ['place_name'],
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(default=None, upload_to='images/', verbose_name='Изображение')),
                ('ordinal', models.PositiveIntegerField(db_index=True, default=1, verbose_name='Порядковый номер')),
                ('description', models.CharField(blank=True, max_length=255, verbose_name='Описание изображения')),
                ('location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='images', to='places.place', verbose_name='Локация')),
            ],
            options={
                'ordering': ['ordinal', 'location__place_name'],
                'unique_together': {('location', 'ordinal')},
            },
        ),
    ]
