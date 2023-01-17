import logging

from .exceptions import GosundException

logger = logging.getLogger('gosundpy')

class GosundDevice(object):

    @staticmethod
    def from_response(resp, device_id, gosund):
        category = resp['result']['category']
        if category == 'cz':
            cls = GosundSwitchDevice
        elif category == 'dj':
            cls = GosundLightBulbDevice
        elif category == 'wsdcg':
            cls = GosundTempuratureHumiditySensorDevice
        elif category == 'ldcg':
            cls = GosundLightSensorDevice
        elif category == 'pir':
            cls = GosundMotionSensorDevice
        elif category == 'mcs':
            cls = GosundContactSensorDevice
        else:
            cls = GosundDevice
        return cls(device_id, gosund)

    def __init__(self, device_id, gosund):
        self.device_id = device_id
        self.gosund = gosund

    def get_status_value(self, code):
        for status in self.gosund.get_device_status(self.device_id):
            if status.get('code') == code:
                return status.get('value')
        raise GosundException(
                f'code "{code}" not found for device id "{self.device_id}"')

    def send_commands(self, commands):
        return self.gosund.send_commands(self.device_id, commands)

    def __str__(self):
        return f'<{self.__class__.__name__} device_id={self.device_id}>'
    __repr__ = __str__

class DeviceOnOffMixin(object):

    def turn_on(self):
        logger.debug('turning on device %s', self.device_id)
        commands = [{'code': self.on_off_code, 'value': True}]
        return self.send_commands(commands)

    def turn_off(self):
        logger.debug('turning off device %s', self.device_id)
        commands = [{'code': self.on_off_code, 'value': False}]
        return self.send_commands(commands)

    def is_on(self):
        return self.get_status_value(self.on_off_code)

    def switch(self):
        logger.debug('switching device %s', self.device_id)
        value = not self.is_on()
        commands = [{'code': self.on_off_code, 'value': value}]
        return self.send_commands(commands)

class GosundSwitchDevice(GosundDevice, DeviceOnOffMixin):

    on_off_code = 'switch_1'

class GosundLightBulbDevice(GosundDevice, DeviceOnOffMixin):

    on_off_code = 'switch_led'

class GosundTempuratureHumiditySensorDevice(GosundDevice):

    temperature_code = 'va_temperature'
    humidity_code = 'va_humidity'

    def get_temperature(self, unit='F'):
        val = self.get_status_value(self.temperature_code)
        temp = val / 10
        if unit.upper() == 'F':
            temp = temp * 9/5 + 32
        return temp

    def get_humidity(self):
        return self.get_status_value(self.humidity_code)

class GosundLightSensorDevice(GosundDevice):

    lux_code = 'bright_value'

    def get_lux(self):
        return self.get_status_value(self.lux_code)

class GosundMotionSensorDevice(GosundDevice):

    motion_code = 'pir'

    NO_ONE_STATE = 'none'
    HUMAN_STATE = 'pir'

    def motion_sensed(self):
        return self.get_status_value(self.motion_code) == self.HUMAN_STATE

class GosundContactSensorDevice(GosundDevice):

    contact_code = 'doorcontact_state'

    def is_open(self):
        return self.get_status_value(self.contact_code)
