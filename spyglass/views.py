from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import redirect
from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.utils.timezone import now
from django.utils.timezone import timedelta
from tastypie.models import ApiKey
from .forms import QueryForm
from .utils import conditionally
from .models import Crawler

@login_required
def change_crawlie_access(request, uid, action):
    if not request.user.is_staff:
        raise PermissionDenied

    if action == '0':
        # Delete a crawler and release the Api Key
        api_key_to_change = get_object_or_404(ApiKey, user_id=uid)
        crawler_to_delete = get_object_or_404(Crawler, \
                                            api_key=api_key_to_change.key)
        crawler_to_delete.delete()
        api_key_to_change.key = None
        api_key_to_change.save()
    elif action == '1':
        # Create a crawler and assign an Api Key
        api_key_to_add = get_object_or_404(ApiKey, user_id=uid)
        new_cr_c = Crawler()
        new_cr_c.api_key = api_key_to_add.key
        new_cr_c.next_refresh = now()
        new_cr_c.save()
    else:
        raise Http404
    return redirect('admin_panel')


@login_required
def admin_panel(request):
    if not getattr(settings, 'SPYGLASS_ADMIN_PANEL', False):
        raise PermissionDenied
    if not request.user.is_staff:
        raise PermissionDenied

    final_data = {}
    for key in ApiKey.objects.all():
        data = {}
        data['email'] = key.user.email
        data['uid'] = key.user.id
        data['api_key'] = key.key
        data['able'] = False
        final_data[key.key] = data
        time = now()
    for crawl in Crawler.objects.all():
        difftime = time - crawl.last_seen
        final_data[crawl.api_key]['last_seen'] = crawl.last_seen
        final_data[crawl.api_key]['active'] = \
                            difftime < timedelta(minutes=10)
        final_data[crawl.api_key]['able'] = True
    final_data = sorted(final_data.items(), \
                            key=lambda y: not y[1]['able'])
        #return HttpResponse(final_data)
    return render_to_response("admin_panel.html", locals(), \
                                context_instance=RequestContext(request))


# Receive a query from a user
@conditionally(login_required, getattr(settings,
                                       'SPYGLASS_AUTHORIZED_QUERIES', True))
def receive_query(request):
    if request.method == 'POST':
        form = QueryForm(request.POST)
        if form.is_valid():
            query = form.save(commit=False)
            mail = form.data['email']

            # If SPYGLASS_ADD_USERS
            if getattr(settings, 'SPYGLASS_ADD_USERS', False):
                # Create the user if he doesnt exist
                defaults={'username':mail.split('@')[0]}
                query.user, created = User.objects.get_or_create(email=mail,
                                                             defaults=defaults)
                if not created and query.user != request.user:
                    raise PermissionDenied
            else:
                # raise Unauthorized if he's not request.user or doesnt exist
                try:
                    query.user =  User.objects.get(email=mail)
                    if query.user != request.user:
                        raise PermissionDenied
                except (User.DoesNotExist):
                    raise PermissionDenied
            query.completed = False
            query.result = None
            query.last_mod = now()
            query.save()
            return redirect(reverse('thanks'))
    # if form is invalid or request is GET, redirect to /
    return redirect('/')
