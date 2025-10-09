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
