def test_temperature_humidity_sensor(gosund, temp_humidity_id):

    device = gosund.get_device(temp_humidity_id)

    val = device.get_temperature()
    assert input(f'is the temperature currently {val}°F? [Y/n] ') in ['y', 'Y', '']

    val = device.get_humidity()
    assert input(f'is the humidity currently {val}%? [Y/n] ') in ['y', 'Y', '']
