"""
URL Configuration for Observations App

Defines URL patterns for all observation-related views including:
- Adding new observations with dynamic form selection
- Listing observations with filtering and infinite scroll
- Viewing/editing observation details with inline editing
- Deleting observations with AJAX confirmation

URL Patterns:
- /observations/add/ - Add new observation form
- /observations/list/ - List all observations with filters
- /observations/detail/<obs_type>/<obs_id>/ - View/edit specific observation
- /observations/delete/<obs_type>/<obs_id>/ - Delete specific observation

The observation type parameter supports: 'star', 'deepsky', 'planet', 'moon', 'sun'
corresponding to the different astronomical object models.
"""

from django.urls import path
from .views import (
    AddObservationView,
    ObservationListView,
    ObservationDetailView,
    DeleteObservationView,
)

urlpatterns = [
    path("add/", AddObservationView.as_view(), name="add_observation"),
    path("list/", ObservationListView.as_view(), name="observation_list"),
    # use unique PK present for each entry in an observation model, to build a unique url
    path(
        "detail/<str:obs_type>/<int:obs_id>/",
        ObservationDetailView.as_view(),
        name="observation_detail",
    ),
    path(
        "delete/<str:obs_type>/<int:obs_id>/",
        DeleteObservationView.as_view(),
        name="delete_observation",
    ),
]
