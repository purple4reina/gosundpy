import json
import pytest
import requests
import responses

from gosundpy.gosund import Gosund

BASEURL = 'https://openapi.tuyaus.com/v1.0/iot-03'

@pytest.fixture
def gosund():
    return _gosund()

@pytest.fixture
def gosund2():
    return _gosund()

@pytest.fixture
def gosund_non_caching():
    return _gosund(caching_secs=None)

@pytest.fixture
def gosund_timeout(monkeypatch):
    timeouts = []
    _orig_request = requests.Session.request
    def _request(*args, timeout=None, **kwargs):
        timeouts.append(timeout)
        return _orig_request(*args, timeout=timeout, **kwargs)
    monkeypatch.setattr('requests.Session.request', _request)
    gosund = _gosund(timeout=10)
    gosund.timeouts = timeouts
    return gosund

@responses.activate
def _gosund(caching_secs=60, timeout=None):
    users_login_uri = f'{BASEURL}/users/login'
    responses.add(
            responses.POST,
            users_login_uri,
            json={'success': True},
            status=200,
    )
    return Gosund('username', 'password', 'access_id', 'access_key',
            status_cache_seconds=caching_secs, timeout=timeout)

def patch_get_device(device_id, category):
    responses.add(
            responses.GET,
            f'{BASEURL}/devices/{device_id}/functions',
            body=json.dumps({'success': True, 'result': {'category': category}}),
            status=200,
    )

def patch_status(*device_ids, resp_json):
    responses.add(
            responses.GET,
            f'{BASEURL}/devices/status?device_ids={",".join(device_ids)}',
            json=resp_json,
            status=200,
    )

@responses.activate
def _get_device(gosund, device_id, category):
    patch_get_device(device_id, category)
    return gosund.get_device(device_id)

@pytest.fixture
def gosund_device(gosund):
    return _get_device(gosund, 'gosund device id', 'ab')

@pytest.fixture
def gosund_temp_sensor(gosund):
    return _get_device(gosund, 'gosund temp sensor device id', 'wsdcg')

@pytest.fixture
def gosund_light_sensor_device(gosund):
    return _get_device(gosund, 'gosund light sensor device', 'ldcg')

@pytest.fixture
def gosund_motion_sensor_device(gosund):
    return _get_device(gosund, 'gosund motion sensor device', 'pir')

@pytest.fixture
def gosund_contact_sensor_device(gosund):
    return _get_device(gosund, 'gosund contact sensor device', 'mcs')
