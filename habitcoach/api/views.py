from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from habitcoach.models import Habit, HabitCompletion, EnvironmentTrigger
from .serializers import (
    HabitSerializer,
    HabitCompletionSerializer,
    EnvironmentTriggerSerializer,
)
from datetime import datetime
from django.db import models


class HabitViewSet(viewsets.ModelViewSet):
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Calculate initial score based on difficulty
        difficulty = serializer.validated_data.get("difficulty", 1)
        reliability_score = 1.0 / difficulty
        serializer.save(user=self.request.user, reliability_score=reliability_score)


class HabitCompletionViewSet(viewsets.ModelViewSet):
    serializer_class = HabitCompletionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return HabitCompletion.objects.filter(habit__user=self.request.user)

    def perform_create(self, serializer):
        habit = serializer.validated_data["habit"]

        # Calculate weighted score
        mood = serializer.validated_data.get("mood", 3)
        score = (habit.difficulty * 2) + (mood * 0.5)

        # Update habit streak and reliability
        habit.streak += 1
        habit.reliability_score = (habit.reliability_score * 0.7) + (score * 0.3)
        habit.save()

        serializer.save(score=score)


class EnvironmentTriggerViewSet(viewsets.ModelViewSet):
    serializer_class = EnvironmentTriggerSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return EnvironmentTrigger.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SuggestionViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        # ML/AI suggestion logic (simplified)
        habits = Habit.objects.filter(user=request.user)

        if not habits.exists():
            suggestions = [
                "Start with a morning routine",
                "Drink 8 glasses of water daily",
            ]
        else:
            # Simple AI: suggest based on time of day
            current_hour = datetime.now().hour
            if current_hour < 12:
                time_based = "Morning meditation"
            elif current_hour < 18:
                time_based = "Afternoon walk"
            else:
                time_based = "Evening journaling"

            suggestions = [
                f"Based on your habits: {time_based}",
                "Try a new habit: Read 10 pages daily",
            ]

        return Response({"suggestions": suggestions})


class DashboardViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        habits = Habit.objects.filter(user=request.user)
        completions = HabitCompletion.objects.filter(habit__user=request.user)

        # User stats
        user_stats = {
            "total_habits": habits.count(),
            "total_completions": completions.count(),
            "avg_reliability": habits.aggregate(models.Avg("reliability_score"))[
                "reliability_score__avg"
            ]
            or 0,
            "longest_streak": habits.aggregate(models.Max("streak"))["streak__max"]
            or 0,
        }

        # Population patterns (simulated)
        population_patterns = {
            "avg_difficulty": 2.8,
            "completion_rate": 0.65,
            "popular_habits": ["Exercise", "Reading", "Meditation"],
        }

        return Response(
            {"user_stats": user_stats, "population_patterns": population_patterns}
        )
