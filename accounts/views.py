from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import RegisterForm, UserSettingsForm
from .models import UserSettings


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Аккаунт создан.")
            return redirect("dashboard")
    else:
        form = RegisterForm()

    return render(request, "accounts/register.html", {"form": form})


@login_required
def profile_view(request):
    settings, created = UserSettings.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = UserSettingsForm(request.POST, instance=settings)

        if form.is_valid():
            form.save()
            messages.success(request, "Настройки сохранены.")
            return redirect("profile")
    else:
        form = UserSettingsForm(instance=settings)

    return render(request, "accounts/profile.html", {
        "form": form,
        "user_profile": settings,
    })


@login_required
def delete_account_view(request):
    if request.method == "POST":
        user = request.user
        user.delete()
        messages.success(request, "Аккаунт удалён.")
        return redirect("landing")

    return render(request, "accounts/delete_account.html")