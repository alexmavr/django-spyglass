from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
from django.conf import settings
from .forms import QueryForm
from .utils import add_users
from .utils import conditionally


def change_crawlie_access(request):
    return request

def admin_panel(request):
    return request

# Receive a query from a user
@conditionally(login_required, getattr(settings,
                                       'SPYGLASS_AUTHORIZED_QUERIES', True))
def receive_query(request):
    if request.method == 'POST':
        form = QueryForm(request.POST)
        if form.is_valid():
            query = form.save(commit=False)
            mail = form.data['email']
            # If adding new users
            if add_users():
                #Create the user if he doesnt exist
                defaults={'username':mail.split('@')[0]}
                query.user, created = User.objects.get_or_create(email=mail,
                                                             defaults=defaults)
                if not created and query.user != request.user:
                    return HttpResponse(status=401)
            else:
                # raise http 401 if he's not request.user or doesnt exist
                try:
                    query.user =  User.objects.get(email=mail)
                    if query.user != request.user:
                        raise PermissionDenied
                except (User.DoesNotExist, PermissionDenied):
                    return HttpResponse(status=401)
            query.completed = False
            query.result = None
            query.last_mod = now()
            query.save()
            return redirect('thanks')
    # if form is invalid or request is GET, redirect to /
    return redirect('/')
