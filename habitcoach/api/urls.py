from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    HabitViewSet,
    HabitCompletionViewSet,
    EnvironmentTriggerViewSet,
    SuggestionViewSet,
    DashboardViewSet,
)

router = DefaultRouter()
router.register(r"habits", HabitViewSet, basename="habit")
router.register(r"completions", HabitCompletionViewSet, basename="completion")
router.register(r"triggers", EnvironmentTriggerViewSet, basename="trigger")
router.register(r"suggestions", SuggestionViewSet, basename="suggestion")
router.register(r"dashboard", DashboardViewSet, basename="dashboard")

urlpatterns = [
    path("", include(router.urls)),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
