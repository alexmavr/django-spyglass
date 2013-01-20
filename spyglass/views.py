from django.contrib.auth.models import User
from django.shortcuts import render_to_response
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
            existing = User.objects.get(email=mail)
            if existing:
                query.user = existing
            else:
                query.user = User.objects.create_user(mail.split('@')[0],
                                                      mail,
                                                      mail + 'pass')
            # Initialize misc Query fields
            query.completed = False
            query.result = None
            query.last_mod = now()

            query.save()
            return render_to_response('messages/thanks.html')
    return redirect('/')

