from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
from .forms import QueryForm
from .app_settings import SPYGLASS_AUTHORIZED_QUERIES
from .app_settings import SPYGLASS_ADD_USERS
from .utils import conditional_decorator

def change_crawlie_access(request):
    return request

def admin_panel(request):
    return request

@conditional_decorator(login_required, SPYGLASS_AUTHORIZED_QUERIES)
def receive_query(request):
    if request.method == 'POST':
        form = QueryForm(request.POST)
        if form.is_valid():
            # Add user to Query or create a new user
            query = form.save(commit=False)
            mail = form.data['email']
            query.user, created = User.objects.get_or_create(email=mail,
                            defaults={'username':mail.split('@')[0],
                                      'password':mail.split('@')[0] +'pass'
                                     })
            query.completed = False
            query.result = None
            query.last_mod = now()
            query.save()
            return redirect('thanks')
    return redirect('/')

