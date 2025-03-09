from django.db import models



class Place(models.Model):
    '''Модель для хранения локаций'''
    place_name = models.CharField(max_length=255, verbose_name='Название локации')
    
    
    def __str__(self):
        return self.place_name


class Image(models.Model):
    '''Модель для хранения изображений'''
    img_id = models.PositiveIntegerField(editable=True, verbose_name='Номер изображения', default=1)
    location = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='images', verbose_name='Локация', null=True, blank=True)
    img_description = models.CharField(max_length=255, verbose_name='Описание изображения', blank=True)
    image = models.ImageField(verbose_name='Файл изображения', null=True, blank=True)       
    
    class Meta:
        unique_together = ('location', 'img_id')
        ordering = ['location__place_name', 'img_id']
            
    def __str__(self):
        return f'{self.img_id} {self.location.place_name}'

    
