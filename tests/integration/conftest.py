import pytest

from integration_env import (USERNAME, PASSWORD, ACCESS_ID, ACCESS_KEY,
        SWITCH_ID, LIGHT_BULB_ID, TEMP_HUMIDITY_ID)
from gosundpy import Gosund

@pytest.fixture
def gosund():
    return Gosund(USERNAME, PASSWORD, ACCESS_ID, ACCESS_KEY)

@pytest.fixture
def switch_id():
    return SWITCH_ID

@pytest.fixture
def light_bulb_id():
    return LIGHT_BULB_ID

@pytest.fixture
def temp_humidity_id():
    return TEMP_HUMIDITY_ID
