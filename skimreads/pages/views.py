from django.shortcuts import render_to_response
from django.template import RequestContext

def about(request):
    """About page."""
    d = {
        'title': 'About Skimreads',
    }
    return render_to_response('pages/about.html', d, 
        context_instance=RequestContext(request))