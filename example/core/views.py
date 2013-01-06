from django.shortcuts import render_to_response

def landing(request):
    return render_to_response("landing.html")
