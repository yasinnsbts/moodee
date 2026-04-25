from django.shortcuts import render

# Create your views here.
from datetime import timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import MoodEntryForm
from .models import MoodEntry


@login_required
def dashboard_view(request):
    today = timezone.localdate()
    week_start = today - timedelta(days=6)

    latest_entries = MoodEntry.objects.filter(
        user=request.user,
    ).order_by("-date", "-created_at")[:5]

    weekly_average = MoodEntry.objects.filter(
        user=request.user,
        date__gte=week_start,
        date__lte=today,
    ).aggregate(avg=Avg("mood_score"))["avg"]

    context = {
        "latest_entries": latest_entries,
        "weekly_average": round(weekly_average, 1) if weekly_average else None,
    }

    return render(request, "mood/dashboard.html", context)


@login_required
def entry_create_view(request):
    if request.method == "POST":
        form = MoodEntryForm(request.POST)

        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.save()

            messages.success(request, "Запись сохранена.")
            return redirect("dashboard")
    else:
        form = MoodEntryForm(initial={"date": timezone.localdate()})

    return render(
        request,
        "mood/entry_form.html",
        {
            "form": form,
            "title": "Новая запись",
            "subtitle": "Как настроение сегодня?",
        },
    )


@login_required
def entry_update_view(request, pk):
    entry = get_object_or_404(MoodEntry, pk=pk, user=request.user)

    if request.method == "POST":
        form = MoodEntryForm(request.POST, instance=entry)

        if form.is_valid():
            form.save()
            messages.success(request, "Запись обновлена.")
            return redirect("dashboard")
    else:
        form = MoodEntryForm(instance=entry)

    return render(
        request,
        "mood/entry_form.html",
        {
            "form": form,
            "entry": entry,
            "title": "Редактировать запись",
            "subtitle": "Измените настроение, дату или заметку",
        },
    )


@login_required
def entry_delete_view(request, pk):
    entry = get_object_or_404(MoodEntry, pk=pk, user=request.user)

    if request.method == "POST":
        entry.delete()
        messages.success(request, "Запись удалена.")
        return redirect("dashboard")

    return render(request, "mood/entry_confirm_delete.html", {"entry": entry})