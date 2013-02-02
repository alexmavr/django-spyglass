from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.utils.timezone import now
from .forms import QueryForm

def change_crawlie_access(request):
    return request

def admin_panel(request):
    return request

def receive_query(request):
    if request.method == 'POST':
        form = QueryForm(request.POST)
        if form.is_valid():
            query = form.save(commit=False)

            # Add user to Query or create a new user
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

