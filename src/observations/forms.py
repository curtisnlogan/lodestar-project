from django import forms
from django.utils import timezone
from .models import ObservingSession, SolarSystem, Star, DeepSky, SpecialEvent


class ObservingSessionForm(forms.ModelForm):
    """
    Form for creating and editing observing sessions.

    Provides datetime inputs for session start/end times and site name field.
    Automatically sets current UTC time as default for start time on new sessions.
    Includes helpful text to guide users in proper time zone handling.
    """

    class Meta:
        model = ObservingSession
        fields = ("datetime_start_ut", "datetime_end_ut", "site_name")
        # provides user with intuitive date/time picker that isn't user time zone biased
        widgets = {
            "datetime_start_ut": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "datetime_end_ut": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }

    def __init__(self, *args, **kwargs):
        """
        Initialize form with helpful text and default values.

        Sets current UTC time as default start time for new sessions and adds
        helpful guidance text for all fields to ensure proper data entry.
        """
        super().__init__(*args, **kwargs)
        # Set default start time to current UTC time for new sessions
        if not self.instance.pk:
            self.fields["datetime_start_ut"].initial = timezone.now()

        # Add helpful text for the datetime fields
        self.fields["datetime_start_ut"].help_text = (
            "Enter observing session start time in UTC. Current UTC time automatically added."
        )
        self.fields["datetime_end_ut"].help_text = (
            "Enter observing session end time in UTC. Can be estimated or left blank."
        )

        # Add helpful text for the site name field
        self.fields["site_name"].help_text = (
            "The physical location where the observing session will take place."
        )


class SolarSystemForm(forms.ModelForm):
    """
    Form for recording solar system object observations.

    Includes fields specific to planetary observations such as altitude,
    central meridian, phase fraction, and disk diameter. Integrates with
    JPL Horizons API for automatic distance calculations.
    """

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
            "drawing": forms.FileInput(
                attrs={
                    "class": "file:bg-gray-600 file:text-white file:border-0 file:px-3 file:py-1 file:rounded file:mr-3 file:cursor-pointer"
                }
            ),
            "antoniadi_scale": forms.Select(attrs={"class": "appearance-none"}),
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
            "drawing": forms.FileInput(
                attrs={
                    "class": "file:bg-gray-600 file:text-white file:border-0 file:px-3 file:py-1 file:rounded file:mr-3 file:cursor-pointer"
                }
            ),
            "antoniadi_scale": forms.Select(attrs={"class": "appearance-none"}),
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
            "drawing": forms.FileInput(
                attrs={
                    "class": "file:bg-gray-600 file:text-white file:border-0 file:px-3 file:py-1 file:rounded file:mr-3 file:cursor-pointer"
                }
            ),
            "antoniadi_scale": forms.Select(attrs={"class": "appearance-none"}),
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
            "drawing": forms.FileInput(
                attrs={
                    "class": "file:bg-gray-600 file:text-white file:border-0 file:px-3 file:py-1 file:rounded file:mr-3 file:cursor-pointer"
                }
            ),
            "antoniadi_scale": forms.Select(attrs={"class": "appearance-none"}),
        }


class SolarSystemUpdateForm(forms.ModelForm):
    """Form for updating Solar System observations."""

    class Meta:
        model = SolarSystem
        fields = [
            "antoniadi_scale",
            "telescope_size_type",
            "magnification_used",
            "eyepieces_used",
            "filters_used",
            "drawing",
            "additional_notes",
            "altitude_degrees",
            "central_meridian_deg",
            "phase_fraction",
            "disk_diameter_arcsec",
        ]
        widgets = {
            "additional_notes": forms.Textarea(attrs={"rows": 4}),
            "drawing": forms.FileInput(
                attrs={
                    "class": "file:bg-gray-600 file:text-white file:border-0 file:px-3 file:py-1 file:rounded file:mr-3 file:cursor-pointer"
                }
            ),
            "antoniadi_scale": forms.Select(attrs={"class": "appearance-none"}),
        }


class StarUpdateForm(forms.ModelForm):
    """Form for updating Star observations."""

    class Meta:
        model = Star
        fields = [
            "antoniadi_scale",
            "telescope_size_type",
            "magnification_used",
            "eyepieces_used",
            "filters_used",
            "drawing",
            "additional_notes",
            "magnitude_estimate",
            "finder_chart_used",
        ]
        widgets = {
            "additional_notes": forms.Textarea(attrs={"rows": 4}),
            "drawing": forms.FileInput(
                attrs={
                    "class": "file:bg-gray-600 file:text-white file:border-0 file:px-3 file:py-1 file:rounded file:mr-3 file:cursor-pointer"
                }
            ),
            "antoniadi_scale": forms.Select(attrs={"class": "appearance-none"}),
        }


class DeepSkyUpdateForm(forms.ModelForm):
    """Form for updating Deep Sky observations."""

    class Meta:
        model = DeepSky
        fields = [
            "antoniadi_scale",
            "telescope_size_type",
            "magnification_used",
            "eyepieces_used",
            "filters_used",
            "drawing",
            "additional_notes",
            "visibility_rating",
        ]
        widgets = {
            "additional_notes": forms.Textarea(attrs={"rows": 4}),
            "drawing": forms.FileInput(
                attrs={
                    "class": "file:bg-gray-600 file:text-white file:border-0 file:px-3 file:py-1 file:rounded file:mr-3 file:cursor-pointer"
                }
            ),
            "antoniadi_scale": forms.Select(attrs={"class": "appearance-none"}),
        }


class SpecialEventUpdateForm(forms.ModelForm):
    """Form for updating Special Event observations."""

    class Meta:
        model = SpecialEvent
        fields = [
            "antoniadi_scale",
            "telescope_size_type",
            "magnification_used",
            "eyepieces_used",
            "filters_used",
            "drawing",
            "additional_notes",
            "event_name",
        ]
        widgets = {
            "additional_notes": forms.Textarea(attrs={"rows": 4}),
            "drawing": forms.FileInput(
                attrs={
                    "class": "file:bg-gray-600 file:text-white file:border-0 file:px-3 file:py-1 file:rounded file:mr-3 file:cursor-pointer"
                }
            ),
            "antoniadi_scale": forms.Select(attrs={"class": "appearance-none"}),
        }
