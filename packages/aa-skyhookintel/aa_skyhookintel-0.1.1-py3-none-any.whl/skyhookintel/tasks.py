"""Tasks."""

from celery import shared_task

from eveuniverse.models import EveConstellation, EveRegion, EveSolarSystem

from allianceauth.services.hooks import get_extension_logger

from skyhookintel.app_settings import ICE_PLANET_TYPE_ID, LAVA_PLANET_TYPE_ID
from skyhookintel.models import Skyhook

logger = get_extension_logger(__name__)


@shared_task
def my_task():
    """An skyhookintel task."""


@shared_task
def load_region_id_skyhooks(region_id: int):
    """Loads all the possible skyhooks in a region"""
    logger.info("Loading region id %s", region_id)

    region, _ = EveRegion.objects.update_or_create_esi(
        id=region_id, include_children=True
    )
    for constellation in region.eve_constellations.all():
        load_constellation_id_skyhooks.delay(constellation.id)


@shared_task
def load_constellation_id_skyhooks(constellation_id: int):
    """Load all skyhooks in the constellation"""
    logger.info("Loading constellation id %s", constellation_id)

    constellation, _ = EveConstellation.objects.update_or_create_esi(
        id=constellation_id, include_children=True
    )
    for solar_system in constellation.eve_solarsystems.all():
        if solar_system.security_status > 0.0:
            logger.info(
                "Skipping solar system id %s because the security status is %s",
                solar_system.id,
                solar_system.security_status,
            )
        load_solar_system_skyhooks.delay(solar_system.id)


@shared_task
def load_solar_system_skyhooks(solar_system_id: int):
    """Load all skyhooks in the solar system"""
    logger.info("Loading solar system %s", solar_system_id)

    solar_system, _ = EveSolarSystem.objects.update_or_create_esi(
        id=solar_system_id,
        include_children=True,
        enabled_sections=[EveSolarSystem.Section.PLANETS],
    )

    for planet in solar_system.eve_planets.filter(eve_type__id=LAVA_PLANET_TYPE_ID):
        Skyhook.create(planet, Skyhook.PlanetType.LAVA)

    for planet in solar_system.eve_planets.filter(eve_type__id=ICE_PLANET_TYPE_ID):
        Skyhook.create(planet, Skyhook.PlanetType.ICE)
