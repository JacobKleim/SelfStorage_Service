from django.db.models import Count
from django.shortcuts import render
from .models import Box, UserProfile, Storehouse


def view_products(request):
    storehouses = Storehouse.objects.prefetch_related('images').annotate(boxes_count=Count('boxes'))
    store_serialized = []
    for storehouse in storehouses:
        store_serialized.append({
            "id": f"{storehouse.id}",
            "city": storehouse.city,
            "address": storehouse.address,
            "description": storehouse.description,
            "road": storehouse.road,
            "contact_phone": storehouse.contact_phone,
            "temperature": storehouse.temperature,
            "boxes_count": storehouse.boxes_count,
            "images": [image.img.url for image in storehouse.images.all()]
        })

    return render(request, template_name="boxes_t.html", context={'storehouses': store_serialized})
