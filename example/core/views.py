from django.shortcuts import render_to_response
from django.template import RequestContext
from spyglass.forms import QueryForm
from spyglass.models import Query
from django.views.generic import TemplateView
from django_tables2 import RequestConfig
from core.tables import ProfileTable

class thanks(TemplateView):
    template_name="messages/thanks.html"

def landing(request):
    if request.user.is_authenticated():
        form = QueryForm({'email':request.user.email, 'site':1, 'params':' '})
    else:
        form = QueryForm()
    return render_to_response("landing.html", locals(), RequestContext(request))

def profile(request):
    data = ProfileTable(Query.objects.filter(user=request.user))
    RequestConfig(request).configure(data)
    return render_to_response("profile.html",locals(),
                              context_instance=RequestContext(request))
