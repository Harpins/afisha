# Generated by Django 5.1.7 on 2025-03-30 21:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0002_alter_image_options_alter_place_options_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='image',
            old_name='img_description',
            new_name='description',
        ),
        migrations.RenameField(
            model_name='image',
            old_name='image',
            new_name='name',
        ),
        migrations.AlterField(
            model_name='image',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='image', to='places.place', verbose_name='Локация'),
        ),
    ]
