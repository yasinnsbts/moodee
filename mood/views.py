from datetime import timedelta
import csv

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import MoodEntryForm
from .models import MoodEntry


def get_current_streak(user, today):
    dates = set(
        MoodEntry.objects.filter(
            user=user,
            date__lte=today,
        ).values_list("date", flat=True)
    )

    streak = 0
    cursor = today

    while cursor in dates:
        streak += 1
        cursor -= timedelta(days=1)

    return streak


def get_filtered_entries(request):
    entries = MoodEntry.objects.filter(user=request.user).order_by("-date", "-created_at")

    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")
    mood_score = request.GET.get("mood_score")

    if start_date:
        entries = entries.filter(date__gte=start_date)

    if end_date:
        entries = entries.filter(date__lte=end_date)

    if mood_score:
        entries = entries.filter(mood_score=mood_score)

    return entries, start_date or "", end_date or "", mood_score or ""


@login_required
def dashboard_view(request):
    today = timezone.localdate()
    week_start = today - timedelta(days=6)

    latest_entries = MoodEntry.objects.filter(
        user=request.user,
    ).order_by("-date", "-created_at")[:5]

    weekly_stats = MoodEntry.objects.filter(
        user=request.user,
        date__gte=week_start,
        date__lte=today,
    ).aggregate(
        avg_mood=Avg("mood_score"),
        avg_stress=Avg("stress_score"),
        avg_sleep=Avg("sleep_hours"),
        entries_count=Count("id"),
    )

    today_entry = MoodEntry.objects.filter(
        user=request.user,
        date=today,
    ).first()

    context = {
        "latest_entries": latest_entries,
        "today_entry": today_entry,
        "current_streak": get_current_streak(request.user, today),
        "weekly_average": round(weekly_stats["avg_mood"], 1) if weekly_stats["avg_mood"] else None,
        "weekly_stress": round(weekly_stats["avg_stress"], 1) if weekly_stats["avg_stress"] else None,
        "weekly_sleep": round(weekly_stats["avg_sleep"], 1) if weekly_stats["avg_sleep"] else None,
        "weekly_entries_count": weekly_stats["entries_count"],
    }

    return render(request, "mood/dashboard.html", context)


@login_required
def entry_list_view(request):
    entries, start_date, end_date, mood_score = get_filtered_entries(request)

    context = {
        "entries": entries,
        "start_date": start_date,
        "end_date": end_date,
        "mood_score": mood_score,
        "entries_count": entries.count(),
    }

    return render(request, "mood/entry_list.html", context)


@login_required
def entry_export_view(request):
    entries = MoodEntry.objects.filter(
        user=request.user,
    ).order_by("-date", "-created_at")

    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")
    mood_score = request.GET.get("mood_score")

    if start_date:
        entries = entries.filter(date__gte=start_date)

    if end_date:
        entries = entries.filter(date__lte=end_date)

    if mood_score:
        entries = entries.filter(mood_score=mood_score)

    response = HttpResponse(content_type="text/csv; charset=utf-8")
    response["Content-Disposition"] = 'attachment; filename="ladno_mood_entries.csv"'
    response.write("\ufeff")

    writer = csv.writer(response)
    writer.writerow([
        "date",
        "mood_score",
        "wellbeing_score",
        "activity_score",
        "stress_score",
        "anxiety_score",
        "sleep_hours",
        "factors",
        "gratitude",
        "note",
        "created_at",
        "updated_at",
    ])

    for entry in entries:
        writer.writerow([
            entry.date,
            entry.mood_score,
            entry.wellbeing_score,
            entry.activity_score,
            entry.stress_score,
            entry.anxiety_score,
            entry.sleep_hours,
            entry.factors,
            entry.gratitude,
            entry.note,
            entry.created_at,
            entry.updated_at,
        ])

    return response


@login_required
def entry_create_view(request):
    if request.method == "POST":
        form = MoodEntryForm(request.POST, user=request.user)

        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.save()

            messages.success(request, "Запись сохранена.")
            return redirect("dashboard")
    else:
        form = MoodEntryForm(initial={"date": timezone.localdate()}, user=request.user)

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

    if not entry.can_edit:
        messages.error(
            request,
            "Редактирование доступно только в течение 24 часов после создания записи.",
        )
        return redirect("entry_list")

    if request.method == "POST":
        form = MoodEntryForm(request.POST, instance=entry, user=request.user)

        if form.is_valid():
            form.save()
            messages.success(request, "Запись обновлена.")
            return redirect("dashboard")
    else:
        form = MoodEntryForm(instance=entry, user=request.user)

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


@login_required
def entry_export_view(request):
    entries, start_date, end_date, mood_score = get_filtered_entries(request)

    response = HttpResponse(content_type="text/csv; charset=utf-8")
    username = request.user.get_username().split("@")[0]
    safe_username = re.sub(r"[^0-9A-Za-zА-Яа-яЁё_-]+", "_", username).strip("_") or "user"
    exported_at = timezone.localtime().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{safe_username}_{exported_at}_ладно_отчет.csv"
    fallback_filename = f"{safe_username}_{exported_at}_ladno_report.csv"
    response["Content-Disposition"] = (
        f'attachment; filename="{fallback_filename}"; filename*=UTF-8\'\'{quote(filename)}'
    )
    response.write("\ufeff")

    writer = csv.writer(response)
    writer.writerow(
        [
            "date",
            "mood_score",
            "wellbeing_score",
            "activity_score",
            "stress_score",
            "anxiety_score",
            "sleep_hours",
            "factors",
            "gratitude",
            "note",
        ]
    )

    for entry in entries.order_by("date", "created_at"):
        writer.writerow(
            [
                entry.date,
                entry.mood_score,
                entry.wellbeing_score,
                entry.activity_score,
                entry.stress_score,
                entry.anxiety_score,
                entry.sleep_hours or "",
                entry.factors,
                entry.gratitude,
                entry.note,
            ]
        )

    return response
