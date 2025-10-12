# allow for more accurate mathematical calculations
from decimal import Decimal, InvalidOperation

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import IntegrityError, models
from django.utils import timezone
from django.utils.text import slugify

from cloudinary.models import CloudinaryField


class TimestampMixin(models.Model):
    """
    Abstract base model that provides timestamp fields for tracking record lifecycle.

    Adds created_at and updated_at fields to any model that inherits from it.
    """

    created_at = models.DateTimeField(
        auto_now_add=True, help_text="Timestamp indicating when the record was created."
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp indicating when the record was last updated.",
    )

    class Meta:
        abstract = True


class ObservingSession(TimestampMixin, models.Model):
    """
    Represents an astronomical observing session.

    A time-based and location-based container for an individual's
    astronomical observations. Each session can contain multiple
    observations of astronomical objects.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sessions",
    )
    datetime_start_ut = models.DateTimeField(
        db_index=True,
        help_text="Enter observing session start time in UTC.",
    )
    datetime_end_ut = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Enter observing session end time in UTC (fill-in when session ends).",
    )
    site_name = models.CharField(max_length=50, blank=True)
    slug = models.SlugField(blank=True, editable=False, max_length=255, unique=True)

    class Meta:
        ordering = ["-datetime_start_ut"]
        verbose_name = "Observing Session"
        verbose_name_plural = "Observing Sessions"

    def clean(self):
        """Custom validation for observing session."""
        super().clean()

        # Validate that start time is not in the future
        if self.datetime_start_ut and self.datetime_start_ut > timezone.now():
            raise ValidationError(
                {"datetime_start_ut": "Start time cannot be in the future."}
            )

        # Validate that end time is after start time
        if (
            self.datetime_start_ut
            and self.datetime_end_ut
            and self.datetime_end_ut <= self.datetime_start_ut
        ):
            raise ValidationError(
                {"datetime_end_ut": "End time must be after start time."}
            )

    def __str__(self):
        if self.datetime_end_ut:
            end_info = f" to {self.datetime_end_ut.strftime('%Y-%m-%d %H:%M')} UTC"
        else:
            end_info = "ongoing"
        return (
            f"{self.user} — {self.datetime_start_ut.strftime('%Y-%m-%d %H:%M')} UTC {end_info}"
            + (f" @ {self.site_name}" if self.site_name else "")
        )

    def generate_slug(self):
        """Build a unique slug from the username PK and session date."""
        if self.slug:
            return None

        date_part = self.datetime_start_ut.strftime("%Y-%m-%d")
        user_pk = slugify(str(self.user.pk))
        base_slug = f"{user_pk}-{date_part}"

        candidate = base_slug
        # slug generation attempts
        suffix = 1
        # grab all observing sessions so we know which slugs exist currently
        queryset = ObservingSession.objects.all()
        # don't include the slug we are generating in the dataset that is to be checked
        if self.pk:
            queryset = queryset.exclude(pk=self.pk)
        # handles edges cases were observing sessions get created at the same time, by looping through suffix candidates until one that doesn't exist
        while queryset.filter(slug=candidate).exists():
            candidate = f"{base_slug}-{suffix}"
            suffix += 1

        self.slug = candidate

    def save(self, *args, **kwargs):

        attempts_remaining = 5

        while attempts_remaining:
            # 1. catch missing/invalid user-entered fields early, don't check for slug as it doesn't exist yet will throw error
            self.full_clean(exclude=["slug"])
            # 2. only build a slug when we have the key inputs
            self.generate_slug()
            # ensure generated slug is validated
            self.full_clean()
            # attempts to save slug, if unable due to edge cases, reduces attempts remaining. handles all but most extreme edge cases out of scope of this project.
            try:
                return super().save(*args, **kwargs)
            except IntegrityError:
                attempts_remaining -= 1
                # checks for 0 attempts which is falsey
                if not attempts_remaining:
                    raise
                self.slug = None


class ObservationMixin(TimestampMixin, models.Model):
    """
    Provides common astronomical observation fields and functionality.

    Shared by all astronomical observation models (SolarSystem, Star, DeepSky,
    SpecialEvent).
    """

    ANTONIADI_CHOICES = [
        ("I", "I"),
        ("II", "II"),
        ("III", "III"),
        ("IV", "IV"),
        ("V", "V"),
    ]

    session = models.ForeignKey(
        ObservingSession,
        on_delete=models.CASCADE,
        related_name="%(class)s_observations",
    )
    antoniadi_scale = models.CharField(
        max_length=3,
        choices=ANTONIADI_CHOICES,
        blank=True,
        help_text="Antoniadi scale rating for atmospheric seeing conditions during observation (I=perfect, V=very poor)",
    )
    telescope_size_type = models.CharField(
        max_length=50, blank=True, help_text='e.g., "8-inch Newtonian"'
    )
    magnification_used = models.CharField(
        max_length=25, blank=True, help_text='e.g., "150x"'
    )
    eyepieces_used = models.CharField(
        max_length=25, blank=True, help_text='e.g., "25mm Plössl"'
    )
    filters_used = models.CharField(
        max_length=25, blank=True, help_text='e.g., "Moon filter"'
    )
    drawing = CloudinaryField(
        null=True,
        blank=True,
        help_text="Is North marked on your drawing? This keeps it scientifically useful!",
    )
    additional_notes = models.TextField(
        blank=True,
        help_text="Additional observations, impressions, or details about your session.",
    )

    class Meta:
        abstract = True


class ApiMixin(TimestampMixin, models.Model):
    """
    Abstract mixin for SIMBAD/JPLHorizons API data storage and validation.

    SIMBAD API used by Star and DeepSky models to store catalog data, validate
    coordinate fields for Aladin sky atlas display, and calculate stellar distances from parallax. JPLHorizons API used by Solar System object to store catalog data.
    """

    # updated_at field from TimestampMixin not needed
    updated_at = None
    # holds the entire API query data in JSON
    api_payload = models.JSONField(null=True, blank=True)
    distance_light_years = models.DecimalField(
        max_digits=10,
        decimal_places=1,
        null=True,
        blank=True,
        help_text="Distance to object in light-years.",
    )
    distance_miles = models.DecimalField(
        max_digits=25,
        decimal_places=1,
        null=True,
        blank=True,
        help_text="Distance to object in miles",
    )

    class Meta:
        abstract = True

    # decorator turns the return into an attribute that can be accessed easily
    @property
    def has_catalog_data(self):
        """Check if object has been stored"""
        return bool(self.api_payload)

    # data transformation method
    def calculate_distances_from_parallax(self, parallax):
        """Convert parallax to distance in light-years and miles."""

        try:
            parallax_value = Decimal(str(parallax))
        except (TypeError, InvalidOperation):
            raise ValueError(f"Invalid parallax value: {parallax}")

        if parallax_value <= 0:
            raise ValueError(f"Parallax must be positive, got: {parallax_value}")

        distance_light_years = Decimal("3260.0") / parallax_value
        distance_miles = distance_light_years * Decimal("5880000000000")

        self.distance_light_years = distance_light_years
        self.distance_miles = distance_miles
        return self.distance_light_years, self.distance_miles

    def calculate_distances_from_lighttime(self, lighttime_minutes):
        """Convert JPL Horizons lighttime to distance in light-years and miles."""

        try:
            lighttime_value = Decimal(str(lighttime_minutes))
        except (TypeError, InvalidOperation):
            raise ValueError(f"Invalid lighttime value: {lighttime_minutes}")

        if lighttime_value <= 0:
            raise ValueError(f"Lighttime must be positive, got: {lighttime_value}")

        # Convert lighttime minutes to light-years
        # 1 light-year = 525,600 light-minutes (365.25 days * 24 hours * 60 minutes)
        distance_light_years = lighttime_value / Decimal("525600.0")

        # Convert to miles: 1 light-year = 5.88 trillion miles
        distance_miles = distance_light_years * Decimal("5880000000000")

        self.distance_light_years = distance_light_years
        self.distance_miles = distance_miles
        return self.distance_light_years, self.distance_miles


class SolarSystem(ObservationMixin, ApiMixin):
    """
    Represents a solar system object observation within an astronomical observing session.

    This model combines common observation fields from ObservationMixin with
    solar system-specific data like phase and altitude.
    API data at moment of creation, can be stored from NASA's JPL Horizons via ApiMixin.
    """

    SOLAR_SYSTEM_CHOICES = [
        ("sun", "Sun"),
        ("moon", "Moon"),
        ("mercury", "Mercury"),
        ("venus", "Venus"),
        ("mars", "Mars"),
        ("jupiter", "Jupiter"),
        ("saturn", "Saturn"),
        ("uranus", "Uranus"),
        ("neptune", "Neptune"),
        ("other", "Other"),
    ]

    celestial_body = models.CharField(
        max_length=25,
        choices=SOLAR_SYSTEM_CHOICES,
        db_index=True,
    )

    altitude_degrees = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(90)],
        help_text="Object's altitude above horizon in degrees (grab from your astronomy app).",
    )
    central_meridian_deg = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(359.99)],
        help_text="Central meridian longitude - which part of the planet is facing Earth (grab from your astronomy app).",
    )
    phase_fraction = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0.00), MaxValueValidator(1.00)],
        help_text="How much of planet's disk is lit (grab from your astronomy app).",
    )
    disk_diameter_arcsec = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)],
        help_text="How big the planet appeared in arcseconds (grab from your astronomy app).",
    )

    class Meta(ObservationMixin.Meta, ApiMixin.Meta):
        abstract = False
        verbose_name = "Solar System Observation"
        verbose_name_plural = "Solar System Observations"

    def __str__(self):
        return f"{self.celestial_body} observation on {self.session.datetime_start_ut.date()}"


class Star(ObservationMixin, ApiMixin):
    star_name = models.CharField(
        max_length=200,
        help_text='Examples: Sirius, Mira, HD 209458. See <a href="https://cds.unistra.fr/cgi-bin/Dic-Simbad" target="_blank">Dictionary of Nomenclature</a>',
        db_index=True,
    )
    magnitude_estimate = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        null=True,
        blank=True,
        validators=[MinValueValidator(-1.5), MaxValueValidator(15.0)],
        help_text="Visual magnitude estimate: lower numbers = brighter (e.g., Sirius = -1.4, naked eye limit ≈ 6.5, binocular limit ≈ 9.5)",
    )
    finder_chart_used = models.CharField(
        max_length=200,
        blank=True,
        help_text='Finder chart details: e.g., "AAVSO chart 15424 ABC" (for variable stars, optional with other types of stars)',
    )

    class Meta(ObservationMixin.Meta, ApiMixin.Meta):
        abstract = False
        verbose_name = "Star Observation"
        verbose_name_plural = "Star Observations"

    def __str__(self):
        return (
            f"{self.star_name} observation on {self.session.datetime_start_ut.date()}"
        )


class DeepSky(ObservationMixin, ApiMixin):
    object_name = models.CharField(
        max_length=200,
        help_text='Examples: Sirius, M31, MCG+02-60-010. See <a href="https://cds.unistra.fr/cgi-bin/Dic-Simbad" target="_blank">Dictionary of Nomenclature</a>',
        db_index=True,
    )
    visibility_rating = models.CharField(
        max_length=20,
        choices=[
            ("easy", "Easy to see"),
            ("moderate", "Moderate difficulty"),
            ("difficult", "Difficult/faint"),
            ("invisible", "Could not see"),
        ],
        blank=True,
        help_text="How easy was it to see through your telescope?",
    )

    class Meta(ObservationMixin.Meta, ApiMixin.Meta):
        abstract = False
        verbose_name = "Deep Sky Observation"
        verbose_name_plural = "Deep Sky Observations"

    def __str__(self):
        return f"{self.object_name} - {self.session.datetime_start_ut.date()}"


class SpecialEvent(ObservationMixin):
    EVENT_CHOICES = [
        ("comet", "Comet"),
        ("meteor_shower", "Meteor Shower"),
        ("solar_eclipse", "Solar Eclipse"),
        ("lunar_eclipse", "Lunar Eclipse"),
        ("aurora", "Aurora"),
        ("other", "Other Special Event"),
    ]

    event_type = models.CharField(
        max_length=20,
        choices=EVENT_CHOICES,
        help_text="Type of special astronomical event?",
        db_index=True,
    )

    event_name = models.CharField(
        max_length=200,
        blank=True,
        help_text='Event name: e.g. "Comet NEOWISE"',
    )

    class Meta(ObservationMixin.Meta):
        abstract = False
        verbose_name = "Special Event Observation"
        verbose_name_plural = "Special Event Observations"

    def __str__(self):
        if self.event_name:
            return f"({self.event_type}) {self.event_name} observation on {self.session.datetime_start_ut.date()}"
        return (
            f"{self.event_type} observation on {self.session.datetime_start_ut.date()}"
        )
