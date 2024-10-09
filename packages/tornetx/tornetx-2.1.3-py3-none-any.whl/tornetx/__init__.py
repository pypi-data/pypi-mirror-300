# __init__.py dans le dossier tornet

from .tornetx import (
    initialize_environment,
    is_tor_installed,
    ma_ip,
    change_ip_repeatedly,
    stop_services,
    check_internet_connection,
    main
)

from .utils import install_pip, install_requests, install_tor, configure_tor
from .banner import print_banner

# Définit la version du package
__version__ = "2.1.3"
