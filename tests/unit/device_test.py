import pytest
import responses

from gosundpy.device import (GosundDevice, GosundSwitchDevice,
        GosundLightBulbDevice, GosundTempuratureHumiditySensorDevice)
from gosundpy.exceptions import GosundException

BASEURL = 'https://openapi.tuyaus.com/v1.0/iot-03'

_test_gosund_device_from_response = (
        ('cz', 'GosundSwitchDevice'),
        ('dj', 'GosundLightBulbDevice'),
        ('wsdcg', 'GosundTempuratureHumiditySensorDevice'),
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

def _test_sensor_response(key, value, success):
    return {
            'result': [
                {'code': 'battery_state', 'value': 'high'},
                {'code': 'battery_percentage', 'value': 100},
                {'code': 'temp_unit_convert', 'value': 'f'},
                {'code': 'maxtemp_set', 'value': 390},
                {'code': 'minitemp_set', 'value': 0},
                {'code': 'maxhum_set', 'value': 60},
                {'code': 'minihum_set', 'value': 20},
                {'code': 'temp_alarm', 'value': 'cancel'},
                {'code': 'hum_alarm', 'value': 'cancel'},
                {'code': 'temp_periodic_report', 'value': 60},
                {'code': 'hum_periodic_report', 'value': 120},
                {'code': 'temp_sensitivity', 'value': 6},
                {'code': 'hum_sensitivity', 'value': 6},
                {'code': key, 'value': value},
            ],
            'success': success,
            't': 1671166487274,
            'tid': 'c3d3f4ac7cfd11ed8864c6843b9bc2ab',
    }

_test_gosund_tempurature_humidity_sensor_device_get_temperature = (
        ('C', 13.5, True),
        ('F', 56.3, True),
        ('C', None, False),
)

@responses.activate
@pytest.mark.parametrize('unit,expect,success',
        _test_gosund_tempurature_humidity_sensor_device_get_temperature)
def test_gosund_tempurature_humidity_sensor_device_get_temperature(
        unit, expect, success, gosund_temp_sensor):
    responses.add(
            responses.GET,
            f'{BASEURL}/devices/{gosund_temp_sensor.device_id}/status',
            json=_test_sensor_response('va_temperature', 135, success),
            status=200,
    )
    try:
        value = gosund_temp_sensor.get_temperature(unit=unit)
    except GosundException:
        assert not success, 'an exception should not have been raised'
    else:
        assert value == expect

_test_gosund_tempurature_humidity_sensor_device_get_humidity = (
        (43, True),
        (None, False),
)

@responses.activate
@pytest.mark.parametrize('expect,success',
        _test_gosund_tempurature_humidity_sensor_device_get_humidity)
def test_gosund_tempurature_humidity_sensor_device_get_humidity(
        expect, success, gosund_temp_sensor):
    responses.add(
            responses.GET,
            f'{BASEURL}/devices/{gosund_temp_sensor.device_id}/status',
            json=_test_sensor_response('va_humidity', 43, success),
            status=200,
    )
    try:
        value = gosund_temp_sensor.get_humidity()
    except GosundException:
        assert not success, 'an exception should not have been raised'
    else:
        assert value == expect
