from django.urls import path
from .views import CapacitySummary

urlpatterns = [
    path('summary/', CapacitySummary.as_view(), name='capacity-summary'),
]