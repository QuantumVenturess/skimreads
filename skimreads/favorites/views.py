from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template import loader, RequestContext
from readings.models import Reading
from skimreads.utils import add_csrf
from users.utils import add_rep, del_rep

import json

@login_required
def fave(request, slug):
    """Save reading to current user's favorites."""
    reading = get_object_or_404(Reading, slug=slug)
    if request.method == 'POST':
        # Check to see if user already has reading saved to favorites
        try:
            favorite = request.user.favorite_set.get(reading=reading)
            # del rep
            del_rep(request, fv=favorite)
            favorite.delete()
        # If user has not saved reading to favorites
        except ObjectDoesNotExist:
            favorite = request.user.favorite_set.create(reading=reading)
            # add rep
            add_rep(request, fv=favorite)
        d = { 
            'reading': reading,
            'static': settings.STATIC_URL,
        }
        t = loader.get_template('favorites/favorite_form.html')
        context = RequestContext(request, add_csrf(request, d))
        data = {
            'favorite_count': len(request.user.favorite_set.all()),
            'favorite_form': t.render(context),
            'pk': reading.pk,
        }
        return HttpResponse(json.dumps(data), mimetype='application/json')
    return HttpResponseRedirect(reverse('readings.views.detail', 
        args=[reading.slug]))