from django import forms
from django.utils import timezone
from .models import ObservingSession, SolarSystem, Star, DeepSky, SpecialEvent


class ObservingSessionForm(forms.ModelForm):
    class Meta:
        model = ObservingSession
        fields = ("datetime_start_ut", "datetime_end_ut", "site_name")
        # provides user with intuitive date/time picker that isn't user time zone biased
        widgets = {
            "datetime_start_ut": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "datetime_end_ut": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set default start time to current UTC time for new sessions
        if not self.instance.pk:
            self.fields["datetime_start_ut"].initial = timezone.now()

        # Add helpful text for the datetime fields
        self.fields["datetime_start_ut"].help_text = (
            "Enter observing session start time in UTC. Current UTC time automatically added."
        )
        self.fields["datetime_end_ut"].help_text = (
            "Enter observing session end time in UTC. Can be estimated now or entered later when session ends."
        )

        # Add helpful text for the site name field
        self.fields["site_name"].help_text = (
            "The physical location where the observing session will take place."
        )


class SolarSystemForm(forms.ModelForm):
    class Meta:
        model = SolarSystem
        fields = [
            "session",
            "antoniadi_scale",
            "telescope_size_type",
            "magnification_used",
            "eyepieces_used",
            "filters_used",
            "drawing",
            "additional_notes",
            "celestial_body",
            "altitude_degrees",
            "central_meridian_deg",
            "phase_fraction",
            "disk_diameter_arcsec",
        ]
        widgets = {
            "additional_notes": forms.Textarea(attrs={"rows": 4}),
        }


class StarForm(forms.ModelForm):
    class Meta:
        model = Star
        fields = [
            "session",
            "antoniadi_scale",
            "telescope_size_type",
            "magnification_used",
            "eyepieces_used",
            "filters_used",
            "drawing",
            "additional_notes",
            "star_name",
            "magnitude_estimate",
            "finder_chart_used",
        ]
        widgets = {
            "additional_notes": forms.Textarea(attrs={"rows": 4}),
        }


class DeepSkyForm(forms.ModelForm):
    class Meta:
        model = DeepSky
        fields = [
            "session",
            "antoniadi_scale",
            "telescope_size_type",
            "magnification_used",
            "eyepieces_used",
            "filters_used",
            "drawing",
            "additional_notes",
            "object_name",
            "visibility_rating",
        ]
        widgets = {
            "additional_notes": forms.Textarea(attrs={"rows": 4}),
        }


class SpecialEventForm(forms.ModelForm):
    class Meta:
        model = SpecialEvent
        fields = [
            "session",
            "antoniadi_scale",
            "telescope_size_type",
            "magnification_used",
            "eyepieces_used",
            "filters_used",
            "drawing",
            "additional_notes",
            "event_type",
            "event_name",
        ]
        widgets = {
            "additional_notes": forms.Textarea(attrs={"rows": 4}),
        }
