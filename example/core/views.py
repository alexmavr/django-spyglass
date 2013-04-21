from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.http import Http404
from django_tables2 import RequestConfig
from core.tables import ProfileTable
from core.tables import NotificationTable
from spyglass.forms import QueryForm
from spyglass.forms import EditQueryForm
from spyglass.models import Query
from spyglass.models import Notification
from .models import NewsStory

class thanks(TemplateView):
    template_name="messages/thanks.html"

def landing(request):
    if request.user.is_authenticated():
        form = QueryForm({'email':request.user.email, 'site':1, 'params':' '})
    else:
        form = QueryForm()
    return render_to_response("landing.html", locals(), RequestContext(request))

@login_required
def profile(request):
    data = ProfileTable(Query.objects.filter(user=request.user))
    RequestConfig(request, paginate={"per_page": 25}).configure(data)
    return render_to_response("profile.html",locals(),
                              context_instance=RequestContext(request))

@login_required
def notifications(request):
    data = NotificationTable(Notification.objects.filter(user=request.user))
    RequestConfig(request, paginate={"per_page": 25}).configure(data)
    return render_to_response("notifications.html",locals(),
                              context_instance=RequestContext(request))

@login_required
def edit(request,rqid):
    query = get_object_or_404(Query, id=rqid)
    if request.POST:
        form = EditQueryForm(request.POST,instance=query)

        # Process the form
        queryreq = form.save(commit=False)
        queryreq.email = request.user.email
        queryreq.save()

        return render_to_response("messages/thanks.html",locals(), RequestContext(request))
    else:
        form = EditQueryForm(instance=query)
        if request.user == query.user:
            return render_to_response("edit.html",locals(), RequestContext(request))
        else:
            raise Http404

@login_required
def delete(request,rqid):
    query = get_object_or_404(Query, id=rqid)
    if request.user == query.user:
        query.delete()
        return render_to_response("messages/delete.html",locals(), RequestContext(request))
    else:
        raise Http404
