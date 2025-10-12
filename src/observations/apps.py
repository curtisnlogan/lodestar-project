from django.apps import AppConfig


class ObservationsConfig(AppConfig):
    """
    Django app configuration for the observations application.

    Handles the core astronomical observation logging functionality including
    models for different observation types, forms, views, and API integrations
    with SIMBAD and JPL Horizons for automatic data enrichment.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "observations"
