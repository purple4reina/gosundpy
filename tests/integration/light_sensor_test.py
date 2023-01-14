def test_light_sensor(gosund, light_sensor_id):

    device = gosund.get_device(light_sensor_id)

    val = device.get_lux()
    assert input(f'is the lux value currently {val}? [Y/n] ') in ['y', 'Y', '']
