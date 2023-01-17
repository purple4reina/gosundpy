from tuya_iot import TuyaOpenAPI, AuthType, TuyaDeviceManager, TuyaOpenMQ

from .device import GosundDevice
from .exceptions import assert_response_success, GosundException
from .utils import cache_response

class Gosund(object):

    def __init__(self, username, password, access_id, access_key, country=1,
            endpoint='https://openapi.tuyaus.com'):
        self.api = TuyaOpenAPI(endpoint, access_id, access_key,
                auth_type=AuthType.CUSTOM)
        resp = self.api.connect(username, password, country)
        assert_response_success('connect to api', resp)
        self.manager = TuyaDeviceManager(self.api, TuyaOpenMQ(self.api))
        self._known_devices = {}

    def get_device(self, device_id):
        resp = self.manager.get_device_functions(device_id)
        assert_response_success('get device', resp)
        self._add_known_device(device_id)
        return GosundDevice.from_response(resp, device_id, self)

    def get_device_status(self, device_id):
        status = self.get_device_statuses().get(device_id)
        if status is None:
            raise GosundException(
                f'unable to find status for device with id "{device_id}"')
        return status

    @cache_response(seconds=60)
    def get_device_statuses(self):
        # limit 20 device_ids per api call
        resp = self.manager.get_device_list_status(self._known_devices)
        assert_response_success('get device statuses', resp)
        return {device['id']: device['status'] for device in resp.get('result', [])}

    def _add_known_device(self, device_id):
        self._known_devices[device_id] = True
        self._clear_statuses_cache()

    def _remove_known_device(self, device_id):
        del self._known_devices[device_id]
        self._clear_statuses_cache()

    def _clear_statuses_cache(self):
        self.get_device_statuses.clear_cache()

    def send_commands(self, device_id, commands):
        resp = self.manager.send_commands(device_id, commands)
        codes = [f'{cmd["code"]}:{cmd["value"]}' for cmd in commands]
        assert_response_success(f'send {codes} command to device', resp)
        self._clear_statuses_cache()
        return resp
