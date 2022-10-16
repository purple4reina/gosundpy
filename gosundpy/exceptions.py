class GosundException(Exception):
    pass

def assert_response_success(action, response):
    if not response.get('success'):
        err = response.get('msg', 'unknown')
        raise GosundException(f'unable to {action}: {err}')
