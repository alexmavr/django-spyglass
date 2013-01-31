from django.shortcuts import render_to_response
from django.template import RequestContext
from spyglass.forms import QueryForm

from django.views.generic import TemplateView

class thanks(TemplateView):
    template_name="messages/thanks.html"

def landing(request):
    if request.user.is_authenticated():
        form = QueryForm({'email':request.user.email, 'site':1, 'params':' '})
    else:
        form = QueryForm()
    return render_to_response("landing.html", locals(), RequestContext(request))
