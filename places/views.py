from django.shortcuts import render
import json
from .models import Place
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.http.response import HttpResponse

def index(request):
    locations = Place.objects.all()
    geojson_data = {
        "type": "FeatureCollection",
        "features": [location.get_features() for location in locations]
    }
   
    return render(request, "index.html", {"geojson": json.dumps(geojson_data)})


def places(request, place_id):
    place = get_object_or_404(Place, place_id=place_id)
    place_images_list = [str(settings.MEDIA_URL) + str(place_image.image) for place_image in place.images.all()]
    place_json_data = {
        "title": place.place_name,
        "imgs": place_images_list,
        "description_short": place.description_short,
        "description_long": place.description_long,
        "coordinates": {
            "lng": str(place.latitude),
            "lat": str(place.longtitude)
        }
    }
    return HttpResponse(json.dumps(place_json_data, ensure_ascii=False), content_type="application/json")