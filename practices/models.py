from django.db import models

# Create your models here.
from django.db import models


class BreathingPractice(models.Model):
    title = models.CharField(
        max_length=100,
        verbose_name="Название",
    )

    description = models.TextField(
        blank=True,
        verbose_name="Описание",
    )

    cycles = models.PositiveSmallIntegerField(
        default=4,
        verbose_name="Количество циклов",
    )

    duration_minutes = models.PositiveSmallIntegerField(
        default=2,
        verbose_name="Длительность в минутах",
    )

    instruction = models.TextField(
        blank=True,
        verbose_name="Инструкция",
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="Активна",
    )

    class Meta:
        verbose_name = "Дыхательная практика"
        verbose_name_plural = "Дыхательные практики"

    def __str__(self):
        return self.title