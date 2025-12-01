from django.db import models
from django.contrib.auth.models import User


class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    difficulty = models.IntegerField(default=1)  # 1-5
    streak = models.IntegerField(default=0)
    reliability_score = models.FloatField(default=0.0)
    preferred_time = models.TimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class HabitCompletion(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE)
    completed_at = models.DateTimeField(auto_now_add=True)
    mood = models.IntegerField(default=3)  # 1-5 scale
    weather = models.CharField(max_length=50, blank=True)
    location = models.CharField(max_length=100, blank=True)
    score = models.FloatField(default=0.0)


class EnvironmentTrigger(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    trigger_type = models.CharField(max_length=50)  # weather, location, weekday
    value = models.CharField(max_length=100)
    habit_suggestion = models.CharField(max_length=200)
    weight = models.FloatField(default=1.0)
