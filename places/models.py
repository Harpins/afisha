from django.db import models



class Place(models.Model):
    '''Модель для хранения локаций'''
    place_name = models.CharField(max_length=255, verbose_name='Название локации')
    
    def __str__(self):
        return f"{self.place_name}"

