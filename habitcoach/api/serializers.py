from rest_framework import serializers
from django.contrib.auth.models import User
from habitcoach.models import Habit, HabitCompletion, EnvironmentTrigger
from django.utils import timezone


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = "__all__"
        read_only_fields = ["user", "streak", "reliability_score"]

    def validate_difficulty(self, value):
        """Ensure difficulty is between 1 and 5."""
        if value < 1 or value > 5:
            raise serializers.ValidationError("Difficulty must be between 1 and 5.")
        return value


class HabitCompletionSerializer(serializers.ModelSerializer):
    class Meta:
        model = HabitCompletion
        fields = "__all__"
        read_only_fields = ["score"]

    def validate_mood(self, value):
        """Ensure mood is between 1 and 5."""
        if value < 1 or value > 5:
            raise serializers.ValidationError("Mood must be between 1 and 5.")
        return value

    # def validate_score(self, value):
    #     """Score should never be negative."""
    #     if value < 0:
    #         raise serializers.ValidationError("Score cannot be negative.")
    #     return value

    def validate(self, data):
        """
        Prevent duplicate daily completion for the same habit.
        - Only 1 completion per habit per date.
        """
        habit = data.get("habit")
        completed_at = data.get("completed_at", timezone.now())

        if HabitCompletion.objects.filter(
            habit=habit,
            completed_at__date=completed_at.date(),
        ).exists():
            raise serializers.ValidationError(
                "This habit has already been completed today."
            )

        return data


class EnvironmentTriggerSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnvironmentTrigger
        fields = "__all__"
        read_only_fields = ["user"]

    VALID_TRIGGER_TYPES = ["weather", "location", "weekday"]

    def validate_trigger_type(self, value):
        """Ensure trigger_type is one of the allowed values."""
        if value not in self.VALID_TRIGGER_TYPES:
            raise serializers.ValidationError(
                f"Trigger type must be one of: {', '.join(self.VALID_TRIGGER_TYPES)}"
            )
        return value

    def validate_weight(self, value):
        """Weight must be positive."""
        if value <= 0:
            raise serializers.ValidationError("Weight must be greater than 0.")
        return value

    def validate(self, data):
        """
        Prevent duplicate triggers per user.
        Combination: (user, trigger_type, value) must be unique.
        """
        user = self.context["request"].user
        trigger_type = data.get("trigger_type")
        value = data.get("value")

        existing = EnvironmentTrigger.objects.filter(
            user=user,
            trigger_type=trigger_type,
            value=value,
        )

        if self.instance:
            # Exclude the current instance on update
            existing = existing.exclude(id=self.instance.id)

        if existing.exists():
            raise serializers.ValidationError(
                "This environment trigger already exists for the user."
            )

        return data
