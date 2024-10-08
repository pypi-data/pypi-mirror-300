"""App settings."""

from django.conf import settings

EXAMPLE_SETTING_ONE = getattr(settings, "EXAMPLE_SETTING_ONE", None)

ICE_PLANET_TYPE_ID = 12
LAVA_PLANET_TYPE_ID = 2015
