import os

if os.environ.get('GOSUND_DEBUG') in ('True', 'true', '1'):
    import logging, tuya_iot
    tuya_iot.TUYA_LOGGER.setLevel(logging.DEBUG)

from .device import GosundDevice, GosundSwitchDevice
from .exceptions import GosundException
from .gosund import Gosund
from .version import version

__all__ = [
        'GosundDevice',
        'GosundSwitchDevice',
        'GosundException',
        'Gosund',
]

__version__ = version
