from tuya_iot import TuyaOpenAPI, AuthType, TuyaDeviceManager, TuyaOpenMQ

from .device import GosundDevice
from .exceptions import assert_response_success

class Gosund(object):

    def __init__(self, username, password, access_id, access_key, country=1,
            endpoint='https://openapi.tuyaus.com'):
        self.api = TuyaOpenAPI(endpoint, access_id, access_key,
                auth_type=AuthType.CUSTOM)
        resp = self.api.connect(username, password, country)
        assert_response_success('connect to api', resp)
        self.manager = TuyaDeviceManager(self.api, TuyaOpenMQ(self.api))

    def get_device(self, device_id):
        resp = self.manager.get_device_functions(device_id)
        assert_response_success('get device', resp)
        return GosundDevice.from_response(resp, device_id, self.manager)
