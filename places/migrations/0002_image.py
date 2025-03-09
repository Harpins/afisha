# Generated by Django 4.0 on 2025-03-09 17:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img_id', models.PositiveIntegerField(default=1, unique=True, verbose_name='Номер изображения')),
                ('img_description', models.CharField(blank=True, max_length=255, verbose_name='Описание изображения')),
                ('image', models.ImageField(upload_to='', verbose_name='Изображения локации')),
                ('location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='images', to='places.place', verbose_name='Локация')),
            ],
        ),
    ]
