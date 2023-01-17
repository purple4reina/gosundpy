import pytest
import responses

from conftest import patch_status, BASEURL
from gosundpy.device import (GosundDevice, GosundSwitchDevice,
        GosundLightBulbDevice, GosundTempuratureHumiditySensorDevice,
        GosundMotionSensorDevice)
from gosundpy.exceptions import GosundException

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
    gosund = 'testing gosund'

    device = GosundDevice.from_response(resp, device_id, gosund)
    assert device.__class__.__name__ == exp_cls
    assert device.device_id == device_id
    assert device.gosund == gosund

@responses.activate
def test_gosund_device_status_success(gosund_device):
    status = 'status'
    resp_json = {
            'success': True,
            'result': [{'id': gosund_device.device_id, 'status': status}],
    }
    patch_status(gosund_device.device_id, resp_json=resp_json)
    assert gosund_device.get_status() == status

@responses.activate
def test_gosund_device_status_failure(gosund_device):
    msg = 'oops'
    patch_status(gosund_device.device_id, resp_json={'success': False, 'msg': msg})
    try:
        gosund_device.get_status()
    except GosundException as e:
        assert e.args == (f'unable to get device statuses: {msg}',)
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

def _test_sensor_response(device_id, key, value, success):
    return {
            'result': [{
                'id': device_id,
                'status': [
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
            }],
            'success': success,
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
    patch_status(
            gosund_temp_sensor.device_id,
            resp_json=_test_sensor_response(gosund_temp_sensor.device_id, 'va_temperature', 135, success),
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
    patch_status(
            gosund_temp_sensor.device_id,
            resp_json=_test_sensor_response(gosund_temp_sensor.device_id, 'va_humidity', 43, success),
    )
    try:
        value = gosund_temp_sensor.get_humidity()
    except GosundException:
        assert not success, 'an exception should not have been raised'
    else:
        assert value == expect

_test_gosund_light_sensor_device_get_lux = (
        (43, True),
        (None, False),
)

@responses.activate
@pytest.mark.parametrize('expect,success',
        _test_gosund_light_sensor_device_get_lux)
def test_gosund_light_sensor_device_get_lux(expect, success,
        gosund_light_sensor_device):
    patch_status(
            gosund_light_sensor_device.device_id,
            resp_json=_test_sensor_response(gosund_light_sensor_device.device_id, 'bright_value', 43, success),
    )
    try:
        value = gosund_light_sensor_device.get_lux()
    except GosundException:
        assert not success, 'an exception should not have been raised'
    else:
        assert value == expect

_test_gosund_motion_sensor_device_motion_sensed = (
        (GosundMotionSensorDevice.HUMAN_STATE, True, True),
        (GosundMotionSensorDevice.NO_ONE_STATE, False, True),
        (GosundMotionSensorDevice.HUMAN_STATE, None, False),
)

@responses.activate
@pytest.mark.parametrize('value,expect,success',
        _test_gosund_motion_sensor_device_motion_sensed)
def test_gosund_motion_sensor_device_motion_sensed(value, expect, success,
        gosund_motion_sensor_device):
    patch_status(
            gosund_motion_sensor_device.device_id,
            resp_json=_test_sensor_response(gosund_motion_sensor_device.device_id, 'pir', value, success),
    )
    try:
        value = gosund_motion_sensor_device.motion_sensed()
    except GosundException:
        assert not success, 'an exception should not have been raised'
    else:
        assert value == expect

_test_gosund_contact_sensor_is_open = (
        (True, True, True),
        (False, False, True),
        (True, None, False),
)

@responses.activate
@pytest.mark.parametrize('value,expect,success',
        _test_gosund_contact_sensor_is_open)
def test_gosund_contact_sensor_is_open(value, expect, success,
        gosund_contact_sensor_device):
    patch_status(
            gosund_contact_sensor_device.device_id,
            resp_json=_test_sensor_response(gosund_contact_sensor_device.device_id, 'doorcontact_state', value, success),
    )
    try:
        value = gosund_contact_sensor_device.is_open()
    except GosundException:
        assert not success, 'an exception should not have been raised'
    else:
        assert value == expect
