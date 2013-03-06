from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from django.template import loader, RequestContext
from haystack.query import SearchQuerySet

import json
import operator

@login_required
def all(request):
    """Return search results for all readings, notes, topics."""
    query = request.GET.get('q')
    if query:
        queries = [word for word in query.split(' ') if word]
        qs = [(Q(content=q) | Q(content__startswith=q)) for q in queries]
        results = SearchQuerySet().filter(reduce(operator.and_, qs)).order_by(
            '-django_ct')[0:10]
    else:
        results = []
    t = loader.get_template('search/results.html')
    context = RequestContext(request, { 'results': results })
    data = {
        'results': t.render(context),
    }
    return HttpResponse(json.dumps(data), mimetype='application/json')