import pytest
import responses

from gosundpy.device import (GosundDevice, GosundSwitchDevice,
        GosundLightbulbDevice)
from gosundpy.exceptions import GosundException

BASEURL = 'https://openapi.tuyaus.com/v1.0/iot-03'

_test_gosund_device_from_response = (
        ('cz', 'GosundSwitchDevice'),
        ('dj', 'GosundLightbulbDevice'),
        ('ab', 'GosundDevice'),
)

@pytest.mark.parametrize('category,exp_cls', _test_gosund_device_from_response)
def test_gosund_device_from_response(category, exp_cls):
    resp = {'result': {'category': category}}
    device_id = 'testing id'
    manager = 'testing manager'

    device = GosundDevice.from_response(resp, device_id, manager)
    assert device.__class__.__name__ == exp_cls
    assert device.device_id == device_id
    assert device.manager == manager

@responses.activate
def test_gosund_device_status_success(gosund_device):
    status = 'status'
    responses.add(
            responses.GET,
            f'{BASEURL}/devices/{gosund_device.device_id}/status',
            json={'success': True, 'result': status},
            status=200,
    )
    assert gosund_device.get_status() == status

@responses.activate
def test_gosund_device_status_failure(gosund_device):
    msg = 'oops'
    responses.add(
            responses.GET,
            f'{BASEURL}/devices/{gosund_device.device_id}/status',
            json={'success': False, 'msg': msg},
            status=200,
    )
    try:
        gosund_device.get_status()
    except GosundException as e:
        assert e.args == (f'unable to get device status: {msg}',)
    else:
        raise AssertionError('should have raised a GosundException')

@responses.activate
def test_gosund_device_send_commands_success(gosund_device):
    commands = [
            {'code': 'code1', 'value': 'value1'},
            {'code': 'code2', 'value': 'value2'},
    ]
    resp = {'success': True}
    responses.add(
            responses.POST,
            f'{BASEURL}/devices/{gosund_device.device_id}/commands',
            json=resp,
            status=200,
    )
    assert gosund_device.send_commands(commands)

@responses.activate
def test_gosund_device_send_commands_failure(gosund_device):
    commands = [
            {'code': 'code1', 'value': 'value1'},
            {'code': 'code2', 'value': 'value2'},
    ]
    msg = 'oops'
    responses.add(
            responses.POST,
            f'{BASEURL}/devices/{gosund_device.device_id}/commands',
            json={'success': False, 'msg': msg},
            status=200,
    )
    try:
        gosund_device.send_commands(commands)
    except GosundException as e:
        assert e.args == (f"unable to send ['code1:value1', 'code2:value2'] "
                f"command to device: {msg}",)
    else:
        raise AssertionError('should have raised a GosundException')
