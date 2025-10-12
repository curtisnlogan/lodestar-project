"""
Django Admin Configuration for Observations App

Configures Django admin interface for all observation models with:
- Customized list displays showing key observation details
- Filtering options by user, date, and object properties
- Search functionality across observation names and users
- Read-only fields for calculated values and metadata
- Logical ordering by creation date (newest first)

Admin classes provide an intuitive interface for managing:
- Observing sessions and their metadata
- Solar system observations with API integration data
- Stellar observations with distance calculations
- Deep sky object observations with catalog information
- Special astronomical events and phenomena

The interface is optimized for astronomy education and observation tracking.
"""

from django.contrib import admin
from .models import ObservingSession, SolarSystem, Star, DeepSky, SpecialEvent


@admin.register(ObservingSession)
class ObservingSessionAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "datetime_start_ut",
        "datetime_end_ut",
        "site_name",
        "slug",
        "created_at",
        "updated_at",
    )
    list_filter = ("user__username", "datetime_start_ut", "site_name")
    search_fields = ("user__username", "datetime_start_ut", "site_name", "slug")
    readonly_fields = ("slug", "created_at", "updated_at")
    ordering = ("-datetime_start_ut",)


@admin.register(SolarSystem)
class SolarSystemAdmin(admin.ModelAdmin):
    list_display = ("celestial_body", "session", "telescope_size_type", "created_at")
    list_filter = ("celestial_body", "session__datetime_start_ut")
    search_fields = ("celestial_body", "session__user__username")
    readonly_fields = ("created_at", "api_payload")
    ordering = ("-created_at",)


@admin.register(Star)
class StarAdmin(admin.ModelAdmin):
    list_display = ("star_name", "session", "telescope_size_type", "created_at")
    list_filter = ("star_name", "session__datetime_start_ut")
    search_fields = ("star_name", "session__user__username")
    readonly_fields = (
        "created_at",
        "api_payload",
        "distance_light_years",
        "distance_miles",
    )
    ordering = ("-created_at",)


@admin.register(DeepSky)
class DeepSkyAdmin(admin.ModelAdmin):
    list_display = ("object_name", "session", "telescope_size_type", "created_at")
    list_filter = ("object_name", "session__datetime_start_ut")
    search_fields = ("object_name", "session__user__username")
    readonly_fields = (
        "created_at",
        "api_payload",
        "distance_light_years",
        "distance_miles",
    )
    ordering = ("-created_at",)


@admin.register(SpecialEvent)
class SpecialEventAdmin(admin.ModelAdmin):
    list_display = (
        "event_type",
        "event_name",
        "session",
        "telescope_size_type",
        "created_at",
    )
    list_filter = ("event_type", "session__datetime_start_ut")
    search_fields = ("event_name", "session__user__username")
    readonly_fields = ("created_at",)
    ordering = ("-created_at",)
