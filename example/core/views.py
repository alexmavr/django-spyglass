from django.shortcuts import render_to_response
from django.template import RequestContext
from spyglass.forms import QueryForm

def user_input(request):
    if request.user.is_authenticated():
        form = QueryForm({'email':request.user.email, 'site':1, 'params':' '})
    else:
        form = QueryForm()
    return render_to_response("user_input.html", locals(), RequestContext(request))
