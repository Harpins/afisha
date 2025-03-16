from django.shortcuts import render
import json
from .models import Place
from django.shortcuts import get_object_or_404


def index(request):
    locations = Place.objects.all()
    geojson_data = {
        "type": "FeatureCollection",
        "features": [location.get_features() for location in locations]
    }
   
    return render(request, "index.html", {"geojson": json.dumps(geojson_data)})

def places(request, place_id):
    place = get_object_or_404(Place, place_id=place_id)
    return render(request, 'places.html', {'place_name': place.place_name})