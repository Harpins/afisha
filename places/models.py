from django.db import models
from tinymce.models import HTMLField  
    

class Place(models.Model):
    '''Модель для хранения локаций'''
    place_name = models.CharField(max_length=255, verbose_name='Название локации')
    place_id = models.CharField(max_length=255, verbose_name='ID локации', unique=True)
    latitude = models.DecimalField(verbose_name='Широта', decimal_places=14, max_digits=17, default=-90.0)
    longtitude = models.DecimalField(verbose_name='Долгота', decimal_places=14, max_digits=18, default=-180.0)
    description_short = models.CharField(max_length=300, verbose_name='Короткое описание', blank=True, default='')
    description_long = HTMLField(max_length=5000, verbose_name='Длинное описание', blank=True, default='')
    
    class Meta:
        ordering = ['place_id']
    
    def __str__(self):
        return self.place_name
    
    
    def get_features(self):
        return {
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": [str(self.longtitude), str(self.latitude)]},
                "properties": {
                    "title": self.place_name,
                    "placeId": self.place_id,
                    "detailsUrl": f'places/{self.place_id}',
                }
            }
        

class Image(models.Model):
    '''Модель для хранения изображений'''
    image = models.ImageField(verbose_name='Изображение', null=True, blank=True)   
    location = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='images', verbose_name='Локация', null=True, blank=True)
    img_id = models.PositiveIntegerField(editable=True, verbose_name='Номер изображения', default=0, blank=False, null=False)
    img_description = models.CharField(max_length=100, verbose_name='Описание изображения', blank=True, default='')
        
        
    class Meta:
        ordering = ['img_id', 'location__place_name']
            
    def __str__(self):
        return f'{self.pk} {self.location}'

    
