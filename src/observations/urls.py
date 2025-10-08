from django.urls import path
from .views import AddObservationView

urlpatterns = [
    path('add/', AddObservationView.as_view(), name='add_observation'),
]