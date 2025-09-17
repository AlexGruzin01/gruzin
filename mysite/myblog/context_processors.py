from .models import Site

def site_info(request):
    info = Site.objects.first()
    return {'site_info': info}