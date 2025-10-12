from django.shortcuts import render, redirect
from django.views.generic import TemplateView, RedirectView
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.core.exceptions import ValidationError
from django.db.models import Q, Count
from itertools import chain
import logging
from .forms import (
    ObservingSessionForm,
    SolarSystemForm,
    StarForm,
    DeepSkyForm,
    SpecialEventForm,
    SolarSystemUpdateForm,
    StarUpdateForm,
    DeepSkyUpdateForm,
    SpecialEventUpdateForm,
)
from .models import ObservingSession, SolarSystem, Star, DeepSky, SpecialEvent
from allauth.account.forms import LoginForm
from allauth.account.views import LoginView

# Astropy extensions for creating data for the `api_payload` field in relevant observation models
from astroquery.jplhorizons import Horizons
from astroquery.simbad import Simbad

logger = logging.getLogger(__name__)


# renders home.html with observing session form if user is authenticated, login form if not
class Home(TemplateView):
    template_name = "observations/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Only show the observing sessions form if user is logged in
        if self.request.user.is_authenticated:
            context["observing_session_form"] = ObservingSessionForm()
        else:
            context["login_form"] = LoginForm()

        return context

    def post(self, request, **kwargs):
        # Handle login form submission for non-authenticated users
        if not request.user.is_authenticated and "login" in request.POST:
            # Create a login view instance to handle the authentication
            login_view = LoginView()
            login_view.request = request
            login_view.setup(request)

            # Get the form with POST data
            form = login_view.get_form()

            if form.is_valid():
                # Use allauth's form_valid method which handles all the authentication logic
                try:
                    login_view.form_valid(form)
                    # Allauth handles success messages automatically, so we don't add our own
                    return redirect("home")
                except Exception:
                    messages.error(request, "Login failed. Please try again.")
            else:
                # Form is invalid, display errors
                context = self.get_context_data(**kwargs)
                context["login_form"] = form  # Pass the form with errors
                return self.render_to_response(context)

        # Only handle observing session POST if user is authenticated
        if not request.user.is_authenticated:
            messages.warning(request, "You must be logged in to create an observation.")
            return redirect("home")

        form = ObservingSessionForm(request.POST)
        if form.is_valid():
            # Save the form with the current user
            observing_session = form.save(commit=False)
            observing_session.user = request.user
            observing_session.save()
            messages.success(
                request,
                'New observing session created successfully! Click the "My Observations" link to add observations to it.',
            )
            return redirect("home")
        else:
            # If form is invalid, redisplay with errors
            messages.error(request, "Please correct the errors below and try again.")
            # ensures nothing is missing from the template context
            context = self.get_context_data(**kwargs)
            # displays again the users invalid input on form
            context["observing_session_form"] = form
            # renders the template_name with above context
            return self.render_to_response(context)


class AddObservationView(LoginRequiredMixin, TemplateView):
    template_name = "observations/add_observation.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get user's observing sessions for dropdown
        context["observing_sessions"] = ObservingSession.objects.filter(
            user=self.request.user
        ).order_by("-datetime_start_ut")

        # Initialize forms
        context["solar_system_form"] = SolarSystemForm()
        context["star_form"] = StarForm()
        context["deep_sky_form"] = DeepSkyForm()
        context["special_event_form"] = SpecialEventForm()

        # Filter observing session choices to user's sessions only
        for form in [
            context["solar_system_form"],
            context["star_form"],
            context["deep_sky_form"],
            context["special_event_form"],
        ]:
            form.fields["session"].queryset = context["observing_sessions"]

        return context

    def post(self, request, **kwargs):
        observation_type = request.POST.get("observation_type")

        # Determine which form to use based on observation type
        form_map = {
            "solar-system": SolarSystemForm,
            "star": StarForm,
            "deep-sky": DeepSkyForm,
            "special-event": SpecialEventForm,
        }

        if observation_type not in form_map:
            messages.error(request, "Please select a valid observation type.")
            return redirect("add_observation")

        FormClass = form_map[observation_type]
        form = FormClass(request.POST, request.FILES)

        # Filter observing session choices to user's sessions only
        form.fields["session"].queryset = ObservingSession.objects.filter(
            user=request.user
        )

        if form.is_valid():
            # tie validated user form data to variable, don't save yet
            observation = form.save(commit=False)
            # check what type of observation the user has submitted
            if observation_type == "deep-sky":
                try:
                    # Configure SIMBAD to get additional fields we need
                    simbad = Simbad()
                    simbad.add_votable_fields(
                        "parallax",
                        "otype",
                        "sp",
                        "flux(V)",
                        "flux(B)",
                        "flux(R)",
                        "flux(I)",
                    )

                    # Use the user's original object name directly
                    object_name = observation.object_name
                    result_table = simbad.query_object(object_name)

                    if result_table is not None and len(result_table) > 0:
                        api_data = {}
                        for col in result_table.colnames:
                            # Convert each column value to string for JSON storage
                            api_data[col] = str(result_table[col][0])
                        observation.api_payload = api_data

                        logger.info(
                            f"Successfully found SIMBAD data for '{object_name}'"
                        )

                        # Calculate distance if parallax is available
                        if (
                            "plx_value" in result_table.colnames
                            and result_table["plx_value"][0] is not None
                        ):
                            try:
                                parallax_mas = float(result_table["plx_value"][0])
                                if parallax_mas > 0:
                                    observation.calculate_distances_from_parallax(
                                        parallax_mas
                                    )
                            except (ValueError, TypeError):
                                logger.warning(
                                    f"Could not calculate distance for {observation.object_name}"
                                )
                    else:
                        logger.warning(f"No SIMBAD data found for '{object_name}'")

                    observation.save()
                except Exception as e:
                    logger.error(
                        f"Failed to get SIMBAD data for {observation.object_name}: {str(e)}"
                    )
                    # Save observation without API data
                    observation.save()
            elif observation_type == "star":
                try:
                    # Configure SIMBAD to get additional fields we need
                    simbad = Simbad()
                    simbad.add_votable_fields(
                        "parallax",
                        "otype",
                        "sp",
                        "flux(V)",
                        "flux(B)",
                        "flux(R)",
                        "flux(I)",
                    )
                    result_table = simbad.query_object(observation.star_name)
                    if result_table is not None:
                        api_data = {}
                        for col in result_table.colnames:
                            # Convert each column value to string for JSON storage
                            api_data[col] = str(result_table[col][0])
                        observation.api_payload = api_data

                        # Calculate distance if parallax is available
                        if (
                            "plx_value" in result_table.colnames
                            and result_table["plx_value"][0] is not None
                        ):
                            try:
                                parallax_mas = float(result_table["plx_value"][0])
                                if parallax_mas > 0:
                                    observation.calculate_distances_from_parallax(
                                        parallax_mas
                                    )
                            except (ValueError, TypeError):
                                logger.warning(
                                    f"Could not calculate distance for {observation.star_name}"
                                )
                    observation.save()
                except Exception as e:
                    logger.error(
                        f"Failed to get SIMBAD data for {observation.star_name}: {str(e)}"
                    )
                    # Save observation without API data
                    observation.save()
            elif observation_type == "solar-system":
                # grab JPL horizons data from the time the user said their observing session started
                if observation.celestial_body == "other":
                    # Skip API call for custom objects
                    observation.save()
                else:
                    try:
                        # Map Django choice values to JPL Horizons identifiers
                        horizons_id_map = {
                            "sun": "10",  # Sun
                            "moon": "301",  # Moon
                            "mercury": "199",  # Mercury
                            "venus": "299",  # Venus
                            "mars": "499",  # Mars
                            "jupiter": "599",  # Jupiter
                            "saturn": "699",  # Saturn
                            "uranus": "799",  # Uranus
                            "neptune": "899",  # Neptune
                        }

                        horizons_id = horizons_id_map.get(observation.celestial_body)
                        if not horizons_id:
                            raise ValueError(
                                f"No JPL Horizons ID found for {observation.celestial_body}"
                            )

                        obj = Horizons(
                            id=horizons_id,
                            location="@399",  # Earth center
                        )
                        eph = obj.ephemerides()
                        api_data = {}
                        for col in eph.colnames:
                            # Convert each column value to string for JSON storage
                            api_data[col] = str(eph[col][0])
                        observation.api_payload = api_data

                        # Calculate distance if lighttime is available
                        if (
                            "lighttime" in eph.colnames
                            and eph["lighttime"][0] is not None
                        ):
                            try:
                                lighttime_minutes = float(eph["lighttime"][0])
                                if lighttime_minutes > 0:
                                    observation.calculate_distances_from_lighttime(
                                        lighttime_minutes
                                    )
                                    logger.info(
                                        f"Calculated distance for {observation.celestial_body}: {lighttime_minutes} light-minutes"
                                    )
                            except (ValueError, TypeError):
                                logger.warning(
                                    f"Could not calculate distance for {observation.celestial_body}"
                                )

                        observation.save()
                    except Exception as e:
                        logger.error(
                            f"Failed to get JPL Horizons data for {observation.celestial_body}: {str(e)}"
                        )
                        # Save observation without API data
                        observation.save()
            else:
                observation.save()
            messages.success(
                request,
                f'New {observation_type.replace("-", " ")} observation added successfully!',
            )
            return redirect("add_observation")
        else:
            messages.error(
                request,
                "Please correct the highlighted errors by selecting the same form again below.",
            )
            context = self.get_context_data(**kwargs)
            # Replace the form with the one containing errors - convert hyphen to underscore for context key
            context_key = observation_type.replace("-", "_")
            context[f"{context_key}_form"] = form
            return self.render_to_response(context)


class LoginRedirectView(RedirectView):
    """
    Redirects login requests to the homepage.

    This view handles the account_login URL and redirects users
    to the homepage where the login functionality is already available.
    """

    permanent = False
    pattern_name = "home"


class AutoLogoutView(RedirectView):
    """
    Automatically logs out the user and redirects to homepage.

    This view handles the account_logout URL and immediately logs out
    the user without showing a confirmation page.
    """

    permanent = False
    pattern_name = "home"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            logout(request)
            messages.success(request, "You have been successfully signed out.")
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # Handle POST requests (from logout forms) the same way
        if request.user.is_authenticated:
            logout(request)
            messages.success(request, "You have been successfully signed out.")
        return super().get(request, *args, **kwargs)


class ObservationListView(LoginRequiredMixin, TemplateView):
    """
    Display user's observations with filtering and infinite scroll.

    Supports filtering by observing session, object type, object name,
    and displays statistics about total observations.
    """

    template_name = "observations/observation_list.html"

    def get_all_observations(self, user):
        """Get all observations for a user across all types."""
        solar_system = SolarSystem.objects.filter(session__user=user).select_related(
            "session"
        )
        stars = Star.objects.filter(session__user=user).select_related("session")
        deep_sky = DeepSky.objects.filter(session__user=user).select_related("session")
        special_events = SpecialEvent.objects.filter(session__user=user).select_related(
            "session"
        )

        # Combine all observations and sort by session date (most recent first)
        all_observations = list(chain(solar_system, stars, deep_sky, special_events))
        all_observations.sort(key=lambda x: x.session.datetime_start_ut, reverse=True)

        return all_observations

    def filter_observations(self, observations, filters):
        """Apply filters to the observations list."""
        filtered_observations = observations

        # Filter by observing session
        if filters.get("session"):
            filtered_observations = [
                obs
                for obs in filtered_observations
                if str(obs.session.id) == filters["session"]
            ]

        # Filter by object type
        if filters.get("object_type"):
            object_type = filters["object_type"]
            if object_type == "solar_system":
                filtered_observations = [
                    obs for obs in filtered_observations if isinstance(obs, SolarSystem)
                ]
            elif object_type == "star":
                filtered_observations = [
                    obs for obs in filtered_observations if isinstance(obs, Star)
                ]
            elif object_type == "deep_sky":
                filtered_observations = [
                    obs for obs in filtered_observations if isinstance(obs, DeepSky)
                ]
            elif object_type == "special_event":
                filtered_observations = [
                    obs
                    for obs in filtered_observations
                    if isinstance(obs, SpecialEvent)
                ]

        # Filter by object name/search term
        if filters.get("search"):
            search_term = filters["search"].lower()
            filtered_observations = [
                obs
                for obs in filtered_observations
                if self.matches_search_term(obs, search_term)
            ]

        return filtered_observations

    def matches_search_term(self, observation, search_term):
        """Check if observation matches the search term."""
        if isinstance(observation, SolarSystem):
            return search_term in observation.celestial_body.lower()
        elif isinstance(observation, Star):
            return search_term in observation.star_name.lower()
        elif isinstance(observation, DeepSky):
            return search_term in observation.object_name.lower()
        elif isinstance(observation, SpecialEvent):
            name_match = (
                observation.event_name and search_term in observation.event_name.lower()
            )
            type_match = search_term in observation.event_type.lower()
            return name_match or type_match
        return False

    def get_observation_display_data(self, observation):
        """Get display data for an observation."""
        if isinstance(observation, SolarSystem):
            return {
                "type": "Solar System",
                "type_class": "solar_system",
                "object_name": observation.get_celestial_body_display(),
                "specific_name": observation.celestial_body,
            }
        elif isinstance(observation, Star):
            return {
                "type": "Star",
                "type_class": "star",
                "object_name": observation.star_name,
                "specific_name": observation.star_name,
            }
        elif isinstance(observation, DeepSky):
            return {
                "type": "Deep Sky",
                "type_class": "deep_sky",
                "object_name": observation.object_name,
                "specific_name": observation.object_name,
            }
        elif isinstance(observation, SpecialEvent):
            return {
                "type": "Special Event",
                "type_class": "special_event",
                "object_name": observation.event_name
                or observation.get_event_type_display(),
                "specific_name": observation.event_type,
            }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get filters from request
        filters = {
            "session": self.request.GET.get("session", ""),
            "object_type": self.request.GET.get("object_type", ""),
            "search": self.request.GET.get("search", "").strip(),
        }

        # Get all observations for the user
        all_observations = self.get_all_observations(self.request.user)

        # Apply filters
        filtered_observations = self.filter_observations(all_observations, filters)

        # Pagination for infinite scroll
        page = self.request.GET.get("page", 1)
        paginator = Paginator(filtered_observations, 10)  # 10 observations per page
        observations_page = paginator.get_page(page)

        # Prepare observations with display data
        observations_with_data = []
        for obs in observations_page:
            display_data = self.get_observation_display_data(obs)
            observations_with_data.append(
                {"observation": obs, "display_data": display_data}
            )

        # Calculate statistics
        total_observations = len(all_observations)
        filtered_count = len(filtered_observations)

        # Get favorite observation type
        type_counts = {}
        for obs in all_observations:
            display_data = self.get_observation_display_data(obs)
            obs_type = display_data["type"]
            type_counts[obs_type] = type_counts.get(obs_type, 0) + 1

        # Get favorite observation type
        favorite_type = None
        favorite_type_count = 0
        if type_counts:
            favorite_type, favorite_type_count = max(
                type_counts.items(), key=lambda x: x[1]
            )

        # Favorite objects (most observed) with distance info
        object_data = {}
        for obs in all_observations:
            display_data = self.get_observation_display_data(obs)
            name = display_data["specific_name"]

            if name not in object_data:
                object_data[name] = {
                    "count": 0,
                    "distance_miles": None,
                    "display_name": display_data["object_name"],
                }

            object_data[name]["count"] += 1

            # Get distance info if available (prioritize non-null values)
            if (
                hasattr(obs, "distance_miles")
                and obs.distance_miles
                and not object_data[name]["distance_miles"]
            ):
                object_data[name]["distance_miles"] = obs.distance_miles

        # Get top 3 favorite objects with their data
        top_objects = sorted(
            [
                (data["display_name"], data["count"], data["distance_miles"])
                for name, data in object_data.items()
            ],
            key=lambda x: x[1],
            reverse=True,
        )[:3]

        context.update(
            {
                "observations": observations_with_data,
                "observing_sessions": ObservingSession.objects.filter(
                    user=self.request.user
                ).order_by("-datetime_start_ut"),
                "filters": filters,
                "total_observations": total_observations,
                "filtered_count": filtered_count,
                "favorite_type": favorite_type,
                "favorite_type_count": favorite_type_count,
                "top_objects": top_objects,
                "has_next": observations_page.has_next(),
                "next_page_number": (
                    observations_page.next_page_number()
                    if observations_page.has_next()
                    else None
                ),
            }
        )

        return context

    def get(self, request, *args, **kwargs):
        # Handle AJAX requests for infinite scroll
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            context = self.get_context_data(**kwargs)

            # Return JSON response with observations data
            observations_data = []
            for obs_data in context["observations"]:
                obs = obs_data["observation"]
                display_data = obs_data["display_data"]

                observations_data.append(
                    {
                        "session_name": str(obs.session),
                        "session_slug": obs.session.slug,
                        "object_type": display_data["type"],
                        "object_name": display_data["object_name"],
                        "date_time": obs.session.datetime_start_ut.strftime(
                            "%m/%d/%y %H:%M"
                        ),
                        "created_at": obs.created_at.isoformat(),
                        "id": obs.id,
                        "type_class": display_data["type_class"],
                    }
                )

            return JsonResponse(
                {
                    "observations": observations_data,
                    "has_next": context["has_next"],
                    "next_page": context["next_page_number"],
                }
            )

        return super().get(request, *args, **kwargs)


class ObservationDetailView(LoginRequiredMixin, TemplateView):
    """
    Display detailed view of a specific observation with SIMBAD data integration.

    Shows user's observation data on the right side and SIMBAD/API data on the left side.
    Supports all observation types: Solar System, Star, Deep Sky, Special Event.
    """

    template_name = "observations/observation_detail.html"

    def get_observation(self, obs_id, obs_type):
        """Get the specific observation based on ID and type."""
        try:
            if obs_type == "solar_system":
                return SolarSystem.objects.select_related("session").get(
                    id=obs_id, session__user=self.request.user
                )
            elif obs_type == "star":
                return Star.objects.select_related("session").get(
                    id=obs_id, session__user=self.request.user
                )
            elif obs_type == "deep_sky":
                return DeepSky.objects.select_related("session").get(
                    id=obs_id, session__user=self.request.user
                )
            elif obs_type == "special_event":
                return SpecialEvent.objects.select_related("session").get(
                    id=obs_id, session__user=self.request.user
                )
            else:
                return None
        except (
            SolarSystem.DoesNotExist,
            Star.DoesNotExist,
            DeepSky.DoesNotExist,
            SpecialEvent.DoesNotExist,
        ):
            return None

    def get_observation_fields(self, observation):
        """Get formatted fields for display based on observation type."""
        # Session info fields first (read-only)
        session_fields = [
            ("Session Location", observation.session.site_name or "Not specified"),
            (
                "Session Start Date/Time (UTC)",
                observation.session.datetime_start_ut.strftime("%Y-%m-%d %H:%M"),
            ),
            (
                "Session End Date/Time (UTC)",
                (
                    observation.session.datetime_end_ut.strftime("%Y-%m-%d %H:%M")
                    if observation.session.datetime_end_ut
                    else "Ongoing"
                ),
            ),
        ]

        # Equipment and observation details
        base_fields = [
            ("Antoniadi Scale (I-V)", observation.antoniadi_scale or "Not specified"),
            ("Telescope Size/Type", observation.telescope_size_type or "Not specified"),
            ("Magnification Used", observation.magnification_used or "Not specified"),
            ("Eyepieces Used", observation.eyepieces_used or "Not specified"),
            ("Filters Used", observation.filters_used or "Not specified"),
            ("Drawing Upload", "Yes" if observation.drawing else "No"),
            ("Additional Notes", observation.additional_notes or "None"),
        ]

        # Add type-specific fields
        if isinstance(observation, SolarSystem):
            specific_fields = [
                ("Celestial Body", observation.get_celestial_body_display()),
                ("Altitude (degrees)", observation.altitude_degrees or "Not specified"),
                (
                    "Central Meridian (deg)",
                    observation.central_meridian_deg or "Not specified",
                ),
                ("Phase Fraction", observation.phase_fraction or "Not specified"),
                (
                    "Disk Diameter (arcsec)",
                    observation.disk_diameter_arcsec or "Not specified",
                ),
            ]
        elif isinstance(observation, Star):
            specific_fields = [
                ("Star Name", observation.star_name),
                (
                    "Magnitude Estimate",
                    observation.magnitude_estimate or "Not specified",
                ),
                ("Finder Chart Used", observation.finder_chart_used or "Not specified"),
            ]
        elif isinstance(observation, DeepSky):
            specific_fields = [
                ("Object Name", observation.object_name),
                (
                    "Visibility Rating",
                    (
                        observation.get_visibility_rating_display()
                        if observation.visibility_rating
                        else "Not specified"
                    ),
                ),
            ]
        elif isinstance(observation, SpecialEvent):
            specific_fields = [
                ("Event Type", observation.get_event_type_display()),
                ("Event Name", observation.event_name or "Not specified"),
            ]
        else:
            specific_fields = []

        return session_fields + specific_fields + base_fields

    def get_api_placeholder_data(self, observation):
        """Get placeholder data for SIMBAD/API section."""
        if isinstance(observation, SolarSystem):
            return {
                "object_name": f"{observation.get_celestial_body_display()}",
                "api_type": "JPL Horizons",
                "description": f"Solar system object data for {observation.get_celestial_body_display()}",
                "has_aladin": False,  # Solar system objects don't use Aladin
            }
        elif isinstance(observation, Star):
            return {
                "object_name": f"{observation.star_name}",
                "api_type": "SIMBAD",
                "description": f"Stellar data and catalog information for {observation.star_name}",
                "has_aladin": True,
            }
        elif isinstance(observation, DeepSky):
            return {
                "object_name": f"{observation.object_name}",
                "api_type": "SIMBAD",
                "description": f"Deep sky object catalog data for {observation.object_name}",
                "has_aladin": True,
            }
        elif isinstance(observation, SpecialEvent):
            return {
                "object_name": f"{observation.event_name or observation.get_event_type_display()}",
                "api_type": "Event Data",
                "description": f"Special event information for {observation.event_name or observation.get_event_type_display()}",
                "has_aladin": False,
            }

        return {
            "object_name": "Unknown",
            "api_type": "No Data",
            "description": "No API data available",
            "has_aladin": False,
        }

    def get_form_class(self, obs_type):
        """Get the appropriate form class based on observation type."""
        form_map = {
            "solar_system": SolarSystemUpdateForm,
            "star": StarUpdateForm,
            "deep_sky": DeepSkyUpdateForm,
            "special_event": SpecialEventUpdateForm,
        }
        return form_map.get(obs_type)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        obs_id = kwargs.get("obs_id")
        obs_type = kwargs.get("obs_type")

        # Get the observation
        observation = self.get_observation(obs_id, obs_type)

        if not observation:
            context["error"] = (
                "Observation not found or you do not have permission to view it."
            )
            return context

        # Get formatted fields for display
        observation_fields = self.get_observation_fields(observation)

        # Get API placeholder data
        api_data = self.get_api_placeholder_data(observation)

        # Get observation type info
        if isinstance(observation, SolarSystem):
            obs_type_display = "Solar System"
            obs_type_class = "solar_system"
        elif isinstance(observation, Star):
            obs_type_display = "Star"
            obs_type_class = "star"
        elif isinstance(observation, DeepSky):
            obs_type_display = "Deep Sky"
            obs_type_class = "deep_sky"
        elif isinstance(observation, SpecialEvent):
            obs_type_display = "Special Event"
            obs_type_class = "special_event"
        else:
            obs_type_display = "Unknown"
            obs_type_class = "unknown"

        # Create the appropriate form for editing
        FormClass = self.get_form_class(obs_type_class)
        if FormClass:
            if "form" not in context:  # Only create form if not passed from POST
                context["form"] = FormClass(instance=observation)

        # Add read-only session information
        context["session_info"] = {
            "site_name": observation.session.site_name or "Unknown Location",
            "start_time": observation.session.datetime_start_ut,
            "end_time": observation.session.datetime_end_ut,
        }

        context.update(
            {
                "observation": observation,
                "observation_fields": observation_fields,
                "api_data": api_data,
                "obs_type_display": obs_type_display,
                "obs_type_class": obs_type_class,
                "obs_id": obs_id,
                "obs_type": obs_type,
            }
        )

        return context

    def post(self, request, **kwargs):
        """Handle POST requests for updating observations using proper Django forms."""
        obs_id = kwargs.get("obs_id")
        obs_type = kwargs.get("obs_type")

        # Get the observation
        observation = self.get_observation(obs_id, obs_type)

        if not observation:
            messages.error(
                request,
                "Observation not found or you do not have permission to edit it.",
            )
            return redirect("observation_list")

        # Get the appropriate form class
        FormClass = self.get_form_class(obs_type)
        if not FormClass:
            messages.error(request, "Invalid observation type.")
            return redirect("observation_list")

        # Create form with POST data and current observation instance
        form = FormClass(request.POST, request.FILES, instance=observation)

        if form.is_valid():
            try:
                # Save the form (this automatically handles field validation)
                updated_observation = form.save()

                messages.success(
                    request,
                    f"{self.get_observation_type_display(updated_observation)} observation updated successfully!",
                )

                # Return JSON response for AJAX requests
                if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                    return JsonResponse(
                        {
                            "success": True,
                            "message": f"{self.get_observation_type_display(updated_observation)} observation updated successfully!",
                        }
                    )

                # Redirect to the same page for regular form submissions
                return redirect("observation_detail", obs_type=obs_type, obs_id=obs_id)

            except Exception as e:
                logger.error(f"Unexpected error while saving observation: {str(e)}")
                messages.error(
                    request,
                    "An unexpected error occurred while updating the observation.",
                )

                # Return JSON response for AJAX requests
                if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                    return JsonResponse(
                        {
                            "success": False,
                            "message": "An unexpected error occurred while updating the observation.",
                        }
                    )

                # Fall through to show form with errors
        else:
            # Form validation failed - crispy forms will display field-specific errors
            messages.error(
                request,
                "Please correct the highlighted errors below.",
            )

            # Return JSON response for AJAX requests
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return JsonResponse(
                    {
                        "success": False,
                        "message": "Please correct the highlighted errors below.",
                        "field_errors": form.errors,
                    }
                )

        # For form validation errors or exceptions, re-render the page with the form containing errors
        context = self.get_context_data(**kwargs)
        context["form"] = form  # Pass the form with errors and user input preserved
        return self.render_to_response(context)

    def get_observation_type_display(self, observation):
        """Get a display name for the observation type."""
        if isinstance(observation, SolarSystem):
            return "Solar System"
        elif isinstance(observation, Star):
            return "Star"
        elif isinstance(observation, DeepSky):
            return "Deep Sky"
        elif isinstance(observation, SpecialEvent):
            return "Special Event"
        else:
            return "Unknown"


# Delete observation view - handles AJAX requests to delete observations
class DeleteObservationView(LoginRequiredMixin, TemplateView):
    def post(self, request, obs_type, obs_id):
        """Handle deletion of observations via AJAX POST request"""
        try:
            # Map observation types to their respective models
            model_map = {
                "solarsystem": SolarSystem,
                "solar_system": SolarSystem,  # Handle underscore format
                "star": Star,
                "deepsky": DeepSky,
                "deep_sky": DeepSky,  # Handle underscore format
                "specialevent": SpecialEvent,
                "special_event": SpecialEvent,  # Handle underscore format
            }

            # Get the appropriate model
            model_class = model_map.get(obs_type.lower())
            if not model_class:
                logger.error(f"Invalid observation type: {obs_type}")
                return JsonResponse(
                    {"success": False, "error": "Invalid observation type"}, status=400
                )

            logger.info(f"Using model class: {model_class.__name__}")

            # Get the observation and verify ownership
            try:
                observation = model_class.objects.get(
                    id=obs_id, session__user=request.user
                )
            except model_class.DoesNotExist:
                logger.error(
                    f"Observation {obs_id} not found or access denied for user {request.user}"
                )
                return JsonResponse(
                    {
                        "success": False,
                        "error": "Observation not found or you do not have permission to delete it",
                    },
                    status=404,
                )

            # Store info for response before deletion
            # Different models use different field names for the object name
            if obs_type.lower() in ["solarsystem", "solar_system"]:
                obs_name = getattr(observation, "celestial_body", "Unknown Object")
            elif obs_type.lower() == "star":
                obs_name = getattr(observation, "star_name", "Unknown Object")
            elif obs_type.lower() in ["deepsky", "deep_sky"]:
                obs_name = getattr(observation, "object_name", "Unknown Object")
            elif obs_type.lower() in ["specialevent", "special_event"]:
                obs_name = getattr(observation, "event_name", "Unknown Object")
            else:
                obs_name = "Unknown Object"

            logger.info(f"Deleting observation: {obs_name} (ID: {obs_id})")

            # Delete the observation
            observation.delete()
            logger.info(f"Successfully deleted observation {obs_id}")

            return JsonResponse(
                {
                    "success": True,
                    "message": f"Successfully deleted '{obs_name}'.",
                }
            )

        except Exception as e:
            # Log the specific error for debugging
            logger.error(
                f"Error deleting observation {obs_id} of type {obs_type}: {str(e)}"
            )

            return JsonResponse(
                {"success": False, "error": f"An unexpected error occurred: {str(e)}"},
                status=500,
            )
