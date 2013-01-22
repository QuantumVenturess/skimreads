from django.conf import settings
from django.shortcuts import render_to_response
from django.template import RequestContext

def about(request):
    """About page."""
    d = {
        'media_root': settings.MEDIA_ROOT,
        'title': 'About Skimreads',
    }
    return render_to_response('pages/about.html', d, 
        context_instance=RequestContext(request))