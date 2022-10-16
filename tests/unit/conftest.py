import json
import pytest
import responses

from gosundpy.gosund import Gosund

BASEURL = 'https://openapi.tuyaus.com/v1.0/iot-03'

@pytest.fixture
@responses.activate
def gosund():
    users_login_uri = f'{BASEURL}/users/login'
    responses.add(
            responses.POST,
            users_login_uri,
            json={'success': True},
            status=200,
    )
    return Gosund('username', 'password', 'access_id', 'access_key')

@responses.activate
def get_device(gosund, category):
    device_id = 'device_id'
    devices_functions_uri = f'{BASEURL}/devices/{device_id}/functions'
    responses.add(
            responses.GET,
            devices_functions_uri,
            body=json.dumps({'success': True, 'result': {'category': category}}),
            status=200,
    )
    return gosund.get_device(device_id)

@pytest.fixture
def gosund_device(gosund):
    return get_device(gosund, 'ab')
