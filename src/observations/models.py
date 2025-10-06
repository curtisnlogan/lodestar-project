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
        auto_now_add=True,
        help_text="Timestamp indicating when the record was created."
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp indicating when the record was last updated."
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
                {'datetime_start_ut': 'Start time cannot be in the future.'}
            )
        
        # Validate that end time is after start time
        if (self.datetime_start_ut and self.datetime_end_ut and 
            self.datetime_end_ut <= self.datetime_start_ut):
            raise ValidationError(
                {'datetime_end_ut': 'End time must be after start time.'}
            )

    def __str__(self):
        if self.datetime_end_ut:
            end_info = (
                f" to {self.datetime_end_ut.strftime('%Y-%m-%d %H:%M')} UTC"
            )
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
            self.full_clean(exclude=['slug'])
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
    drawing = CloudinaryField(null=True, blank=True, help_text="Is North marked on your drawing? This keeps it scientifically useful!")
    additional_notes = models.TextField(blank=True)

    class Meta:
        abstract = True

# TODO
class ApiMixin(TimestampMixin, models.Model):
    """
    Abstract mixin for SIMBAD/JPLHorizons API data storage and validation.

    SIMBAD API used by Star and DeepSky models to store catalog data, validate
    coordinate fields for Aladin sky atlas display, and calculate stellar distances from parallax. JPLHorizons API used by Solar System object to store catalog data.
    """

    api_payload = models.JSONField(null=True, blank=True)
    distance_light_years = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Distance to star system in light-years calculated from SIMBAD parallax data",
    )
    distance_miles = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Distance to star(s) in miles",
    )

    class Meta:
        abstract = True

    @property
    def has_catalog_data(self):
        """Check if object has been stored"""
        return bool(self.api_payload)

    def calculate_distances_from_parallax(self, parallax_mas):
        """Convert parallax in milliarcseconds to distance in light-years and miles."""
        self.distance_light_years = None
        self.distance_miles = None

        if not self.has_catalog_data:
            return None, None

        if parallax_mas in (None, ""):
            return None, None

        try:
            parallax_value = Decimal(parallax_mas)
        except (TypeError, InvalidOperation):
            return None, None

        if parallax_value <= 0:
            return None, None

        distance_light_years = Decimal("3260.0") / parallax_value
        distance_miles = distance_light_years * Decimal("5880000000000")

        self.distance_light_years = distance_light_years
        self.distance_miles = distance_miles
        return self.distance_light_years, self.distance_miles


class SolarSystem(ObservationMixin, ApiMixin):
    """
    Represents a solar system object observation within an astronomical observing session.

    This model combines common observation fields from ObservationMixin with
    solar system-specific data like phase, altitude, and planetary features.
    API data from NASA's JPL Horizons can be stored via ApiMixin.
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

    @property
    def coordinates(self):
        """Return RA/Dec from cached API payload when available."""
        payload = self.api_payload
        if not payload:
            return None
        ra = payload.get("ra")
        dec = payload.get("dec")
        if ra is None or dec is None:
            return None
        return {"ra": ra, "dec": dec}

    @property
    def aladin_url(self):
        """Generate an Aladin Lite URL for quickly previewing the object."""
        payload = self.api_payload
        if not payload:
            return ""
        payload_get = payload.get
        ra = payload_get("ra")
        dec = payload_get("dec")
        if ra is None or dec is None:
            return ""
        return (
            "https://aladin.u-strasbg.fr/AladinLite/?target="
            f"{ra}%20{dec}&fov=0.2&survey=P%2FDSS2%2Fcolor"
        )

    altitude_degrees = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(90)],
        help_text="Object's altitude above horizon in degrees (grab from your astronomy app)",
    )
    central_meridian_deg = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(360)],
        help_text="Central meridian longitude - which part of the planet is facing Earth (grab from your astronomy app)",
    )
    phase_fraction = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0.00), MaxValueValidator(1.00)],
        help_text="How much of planet's disk is lit (grab from your astronomy app)",
    )
    disk_diameter_arcsec = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="How big the planet appeared in arcseconds (grab from your astronomy app)",
    )
    features_observed = models.TextField(
        blank=True,
        help_text='What did you see? Describe surface features, colors, belts, spots, moons, or other details visible through your telescope. Example for Jupiter: "Great Red Spot prominent, two dark equatorial belts visible, Europa casting shadow on disk, Io just off eastern limb"',
    )

    class Meta(ObservationMixin.Meta, ApiMixin.Meta):
        abstract = False
        verbose_name = "Solar System Observation"
        verbose_name_plural = "Solar System Observations"

    def __str__(self):
        return (
            f"{self.celestial_body} observation on {self.datetime_ut.date()}"
        )
    
    def __repr__(self):
        return f"<SolarSystem(id={self.pk}, body='{self.celestial_body}', date='{self.datetime_ut.date()}')>"


class Star(ObservationMixin, ApiMixin):
    star_name = models.CharField(
        max_length=200,
        help_text='e.g., "Mira"',
        db_index=True,
    )
    magnitude_estimate = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        null=True,
        blank=True,
        help_text="Star's brightness: smaller numbers = brighter (e.g. 2.5)",
    )
    finder_chart_used = models.CharField(
        max_length=200,
        blank=True,
        help_text='Finder chart details: e.g., "AAVSO chart 15424 ABC" (for variable stars, optional with other types of stars)',
    )

    def clean(self):
        """Custom validation for star observations."""
        super().clean()
        
        # Validate magnitude estimate is within reasonable range
        if (self.magnitude_estimate is not None and 
            (self.magnitude_estimate < -30 or self.magnitude_estimate > 30)):
            raise ValidationError(
                {'magnitude_estimate': 'Magnitude must be between -30 and 30.'}
            )

    class Meta(ObservationMixin.Meta, ApiMixin.Meta):
        abstract = False
        verbose_name = "Star Observation"
        verbose_name_plural = "Star Observations"

    def __str__(self):
        return f"{self.star_name} observation on {self.datetime_ut.date()}"


class DeepSky(ObservationMixin, ApiMixin):
    object_name = models.CharField(
        max_length=200,
        help_text='e.g. "Orion Nebula"',
        db_index=True,
    )
    constellation = models.CharField(
        max_length=40, blank=True, help_text='e.g., "Orion"'
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
    sketched_features = models.TextField(
        blank=True,
        help_text="What details did you see? (spiral arms, central bulge, nebulosity, star colors, etc.)",
    )

    class Meta(ObservationMixin.Meta, ApiMixin.Meta):
        abstract = False
        verbose_name = "Deep Sky Observation"
        verbose_name_plural = "Deep Sky Observations"

    def __str__(self):
        if self.constellation:
            return f"{self.object_name} ({self.constellation}) - {self.datetime_ut.date()}"
        return f"{self.object_name} - {self.datetime_ut.date()}"


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
        help_text="Type of special astronomical event",
        db_index=True,
    )

    event_name = models.CharField(
        max_length=200,
        blank=True,
        help_text='Event name: e.g. "C/2020 F3 NEOWISE"',
    )

    class Meta(ObservationMixin.Meta):
        abstract = False
        verbose_name = "Special Event Observation"
        verbose_name_plural = "Special Event Observations"

    def __str__(self):
        if self.event_name:
            return f"{self.event_name} ({self.event_type}) - {self.datetime_ut.date()}"
        return f"{self.event_type} observation on {self.datetime_ut.date()}"
