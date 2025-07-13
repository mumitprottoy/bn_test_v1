from django.http import JsonResponse
from .models import BusinessSponsor


def business_sponsors(request):
    return JsonResponse(dict(
        sponsors=[dict(name=s.name, formal_name=s.formal_name, logo_url=s.logo_url) for s in BusinessSponsor.objects.all()]
    ))

