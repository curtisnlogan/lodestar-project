from django.urls import path
from . import views

urlpatterns = [
    path("", views.AstronomyNewsView.as_view(), name="astronomy_news"),
]
