from django.shortcuts import render

# Create your views here.
from django.shortcuts import render


def landing(request):
    return render(request, "core/landing.html")