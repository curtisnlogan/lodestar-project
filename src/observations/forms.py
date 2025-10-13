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
                    "class": "w-full text-sm text-gray-300 bg-gray-700 border border-gray-600 rounded-lg cursor-pointer focus:outline-none focus:ring-2 focus:ring-yellow-300 file:mr-3 file:py-2 file:px-4 file:rounded-l-lg file:border-0 file:text-sm file:font-medium file:bg-gray-600 file:text-white hover:file:bg-gray-500 file:cursor-pointer overflow-hidden text-ellipsis whitespace-nowrap"
                }
            ),
            "antoniadi_scale": forms.Select(attrs={"class": "appearance-none"}),
        }

    def __init__(self, *args, **kwargs):
        """
        Initialize form with helpful text for solar system observations.

        Adds clear guidance for the celestial body selection and other fields
        to ensure proper data entry and validation feedback.
        """
        super().__init__(*args, **kwargs)

        # Add clear help text indicating celestial body is required
        self.fields["celestial_body"].help_text = (
            "REQUIRED: Select the solar system object you observed. "
            "Choose from planets, the Moon, or the Sun."
        )


class StarForm(forms.ModelForm):
    """
    Form for recording stellar observations.

    Includes fields specific to star observations such as magnitude estimates
    and finder chart information. Integrates with SIMBAD API for automatic
    stellar data retrieval and distance calculations.
    """

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
                    "class": "w-full text-sm text-gray-300 bg-gray-700 border border-gray-600 rounded-lg cursor-pointer focus:outline-none focus:ring-2 focus:ring-yellow-300 file:mr-3 file:py-2 file:px-4 file:rounded-l-lg file:border-0 file:text-sm file:font-medium file:bg-gray-600 file:text-white hover:file:bg-gray-500 file:cursor-pointer overflow-hidden text-ellipsis whitespace-nowrap"
                }
            ),
            "antoniadi_scale": forms.Select(attrs={"class": "appearance-none"}),
        }

    def __init__(self, *args, **kwargs):
        """
        Initialize form with helpful text for stellar observations.

        Adds clear guidance for the star name field and other fields
        to ensure proper data entry and validation feedback.
        """
        super().__init__(*args, **kwargs)

        # Add clear help text indicating star name is required
        self.fields["star_name"].help_text = (
            "REQUIRED: Enter the name of the star you observed. "
            'Examples: Sirius, Mira, HD 209458. See <a href="https://cds.unistra.fr/cgi-bin/Dic-Simbad" target="_blank">Dictionary of Nomenclature</a>'
        )


class DeepSkyForm(forms.ModelForm):
    """
    Form for recording deep sky object observations.

    Includes fields specific to deep sky observations such as visibility ratings
    and object information. Integrates with SIMBAD API for automatic catalog
    data retrieval and distance calculations.
    """

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
                    "class": "w-full text-sm text-gray-300 bg-gray-700 border border-gray-600 rounded-lg cursor-pointer focus:outline-none focus:ring-2 focus:ring-yellow-300 file:mr-3 file:py-2 file:px-4 file:rounded-l-lg file:border-0 file:text-sm file:font-medium file:bg-gray-600 file:text-white hover:file:bg-gray-500 file:cursor-pointer overflow-hidden text-ellipsis whitespace-nowrap"
                }
            ),
            "antoniadi_scale": forms.Select(attrs={"class": "appearance-none"}),
        }

    def __init__(self, *args, **kwargs):
        """
        Initialize form with helpful text for deep sky observations.

        Adds clear guidance for the object name field and other fields
        to ensure proper data entry and validation feedback.
        """
        super().__init__(*args, **kwargs)

        # Add clear help text indicating object name is required
        self.fields["object_name"].help_text = (
            "REQUIRED: Enter the name of the deep sky object you observed. "
            'Examples: Sirius, M31, MCG+02-60-010. See <a href="https://cds.unistra.fr/cgi-bin/Dic-Simbad" target="_blank">Dictionary of Nomenclature</a>'
        )


class SpecialEventForm(forms.ModelForm):
    """
    Form for recording special astronomical event observations.

    Includes fields specific to special events such as meteor showers,
    eclipses, and comet appearances. Provides event type selection
    and optional event naming for cataloging purposes.
    """

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
                    "class": "w-full text-sm text-gray-300 bg-gray-700 border border-gray-600 rounded-lg cursor-pointer focus:outline-none focus:ring-2 focus:ring-yellow-300 file:mr-3 file:py-2 file:px-4 file:rounded-l-lg file:border-0 file:text-sm file:font-medium file:bg-gray-600 file:text-white hover:file:bg-gray-500 file:cursor-pointer overflow-hidden text-ellipsis whitespace-nowrap"
                }
            ),
            "antoniadi_scale": forms.Select(attrs={"class": "appearance-none"}),
        }

    def __init__(self, *args, **kwargs):
        """
        Initialize form with helpful text for special event observations.

        Adds clear guidance for the event type field and other fields
        to ensure proper data entry and validation feedback.
        """
        super().__init__(*args, **kwargs)

        # Add clear help text indicating event type is required
        self.fields["event_type"].help_text = (
            "REQUIRED: Select the type of astronomical event you observed. "
        )


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
                    "class": "w-full text-sm text-gray-300 bg-gray-700 border border-gray-600 rounded-lg cursor-pointer focus:outline-none focus:ring-2 focus:ring-yellow-300 file:mr-3 file:py-2 file:px-4 file:rounded-l-lg file:border-0 file:text-sm file:font-medium file:bg-gray-600 file:text-white hover:file:bg-gray-500 file:cursor-pointer overflow-hidden text-ellipsis whitespace-nowrap"
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
                    "class": "w-full text-sm text-gray-300 bg-gray-700 border border-gray-600 rounded-lg cursor-pointer focus:outline-none focus:ring-2 focus:ring-yellow-300 file:mr-3 file:py-2 file:px-4 file:rounded-l-lg file:border-0 file:text-sm font-medium file:bg-gray-600 file:text-white hover:file:bg-gray-500 file:cursor-pointer overflow-hidden text-ellipsis whitespace-nowrap"
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
                    "class": "w-full text-sm text-gray-300 bg-gray-700 border border-gray-600 rounded-lg cursor-pointer focus:outline-none focus:ring-2 focus:ring-yellow-300 file:mr-3 file:py-2 file:px-4 file:rounded-l-lg file:border-0 file:text-sm file:font-medium file:bg-gray-600 file:text-white hover:file:bg-gray-500 file:cursor-pointer overflow-hidden text-ellipsis whitespace-nowrap"
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
                    "class": "w-full text-sm text-gray-300 bg-gray-700 border border-gray-600 rounded-lg cursor-pointer focus:outline-none focus:ring-2 focus:ring-yellow-300 file:mr-3 file:py-2 file:px-4 file:rounded-l-lg file:border-0 file:text-sm file:font-medium file:bg-gray-600 file:text-white hover:file:bg-gray-500 file:cursor-pointer overflow-hidden text-ellipsis whitespace-nowrap"
                }
            ),
            "antoniadi_scale": forms.Select(attrs={"class": "appearance-none"}),
        }
