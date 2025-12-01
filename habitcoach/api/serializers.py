from rest_framework import serializers
from django.contrib.auth.models import User
from habitcoach.models import Habit, HabitCompletion, EnvironmentTrigger


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = "__all__"
        read_only_fields = ["user", "streak", "reliability_score"]


class HabitCompletionSerializer(serializers.ModelSerializer):
    class Meta:
        model = HabitCompletion
        fields = "__all__"
        read_only_fields = ["score"]


class EnvironmentTriggerSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnvironmentTrigger
        fields = "__all__"
        read_only_fields = ["user"]
