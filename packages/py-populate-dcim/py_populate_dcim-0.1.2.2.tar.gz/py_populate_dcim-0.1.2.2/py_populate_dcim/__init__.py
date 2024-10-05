"""App declaration for py_populate_dcim."""

# Metadata is inherited from Nautobot. If not including Nautobot in the environment, this should be added
from importlib import metadata

from nautobot.apps import NautobotAppConfig
from .navigation import menu_items

__version__ = metadata.version(__name__)


class PyPopulateDcimConfig(NautobotAppConfig):
    """App configuration for the py_populate_dcim app."""

    name = "py_populate_dcim"
    verbose_name = "Etherflow's Python DCIM Populator"
    version = __version__
    author = "Etherflow"
    description = "Merge ACI and OneView by LACP configs... and more!"
    base_url = "py-populate-dcim"
    required_settings = []
    min_version = "2.3.4"
    max_version = "2.9999"
    default_settings = {}
    caching_config = {}
    home_view_name = "plugins:py_populate_dcim:home"
    menu_items = "navigation:menu_items"


config = PyPopulateDcimConfig  # pylint:disable=invalid-name
