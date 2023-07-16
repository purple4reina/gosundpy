class GosundException(Exception):
    pass

class GosundDeviceOfflineException(GosundException):
    pass

def assert_response_success(action, response):
    if not response.get('success'):
        err = response.get('msg', 'unknown')
        if err == 'device is offline':
            raise GosundDeviceOfflineException(f'unable to {action}: {err}')
        raise GosundException(f'unable to {action}: {err}')
