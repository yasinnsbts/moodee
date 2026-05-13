from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import BreathingPractice


@login_required
def practices_view(request):
    practices = BreathingPractice.objects.filter(is_active=True)

    return render(
        request,
        "practices/practices.html",
        {
            "practices": practices,
        },
    )
