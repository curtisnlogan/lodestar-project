from django.core.management.base import BaseCommand
from observations.models import SolarSystem
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Calculate distances for existing solar system observations with JPL Horizons data"

    def handle(self, *args, **options):
        # Find solar system observations that have API data but no distance calculated
        observations = SolarSystem.objects.filter(
            api_payload__isnull=False, distance_light_years__isnull=True
        )

        updated_count = 0

        for observation in observations:
            if observation.api_payload and "lighttime" in observation.api_payload:
                try:
                    lighttime_minutes = float(observation.api_payload["lighttime"])
                    if lighttime_minutes > 0:
                        observation.calculate_distances_from_lighttime(
                            lighttime_minutes
                        )
                        observation.save()
                        updated_count += 1
                        self.stdout.write(
                            self.style.SUCCESS(
                                f"Updated distances for {observation.celestial_body} observation "
                                f"(lighttime: {lighttime_minutes} minutes, "
                                f"distance: {observation.distance_light_years} light-years)"
                            )
                        )
                except (ValueError, TypeError, KeyError) as e:
                    self.stdout.write(
                        self.style.WARNING(
                            f"Could not calculate distance for {observation.celestial_body}: {e}"
                        )
                    )

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully updated distances for {updated_count} solar system observations"
            )
        )
