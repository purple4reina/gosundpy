from .exceptions import assert_response_success

class GosundDevice(object):

    @staticmethod
    def from_response(resp, device_id, manager):
        category = resp['result']['category']
        if category == 'cz':
            cls = GosundSwitchDevice
        else:
            cls = GosundDevice
        return cls(device_id, manager)

    def __init__(self, device_id, manager):
        self.device_id = device_id
        self.manager = manager

    def get_status(self):
        resp = self.manager.get_device_status(self.device_id)
        assert_response_success('get device status', resp)
        return resp.get('result', [])

    def send_commands(self, commands):
        resp = self.manager.send_commands(self.device_id, commands)
        codes = [f'{cmd["code"]}:{cmd["value"]}' for cmd in commands]
        assert_response_success(f'send {codes} command to device', resp)
        return resp

    def __str__(self):
        return f'<{self.__class__.__name__} device_id={self.device_id}>'
    __repr__ = __str__

class GosundSwitchDevice(GosundDevice):

    def turn_on(self):
        commands = [{'code': 'switch_1', 'value': True}]
        return self.send_commands(commands)

    def turn_off(self):
        commands = [{'code': 'switch_1', 'value': False}]
        return self.send_commands(commands)

    def is_on(self):
        for status in self.get_status():
            if status.get('code') == 'switch_1':
                return status.get('value', False)
        return False

    def switch(self):
        value = not self.is_on()
        commands = [{'code': 'switch_1', 'value': value}]
        return self.send_commands(commands)
