# Generated by Django 4.0 on 2025-03-16 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0002_alter_place_place_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='place',
            name='details_url',
        ),
        migrations.AddField(
            model_name='place',
            name='description_long',
            field=models.CharField(blank=True, max_length=2000, null=True, verbose_name='Длинное описание'),
        ),
        migrations.AddField(
            model_name='place',
            name='description_short',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name='Короткое описание'),
        ),
    ]
