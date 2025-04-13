import json
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.http.response import HttpResponse

from .models import Place

def index(request):
    locations = Place.objects.all()
    geojson_data = {
        "type": "FeatureCollection",
        "features": [location.get_features() for location in locations]
    }
   
    return render(request, "index.html", {"geojson": geojson_data})


def place_details(request, place_id):
    place = get_object_or_404(Place, place_id=place_id)
    place_images = [f"{settings.MEDIA_URL}{place_image.image}" for place_image in place.images.all()]
    place_json_data = {
        "title": place.place_name,
        "imgs": place_images,
        "description_short": place.description_short,
        "description_long": place.description_long,
        "coordinates": {
            "lng": str(place.latitude),
            "lat": str(place.longtitude)
        }
    }
    return HttpResponse(json.dumps(place_json_data, ensure_ascii=False), content_type="application/json")