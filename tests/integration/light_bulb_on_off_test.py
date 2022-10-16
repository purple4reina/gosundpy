def test_light_bulb_on_off(gosund, light_bulb_id):

    def assert_on():
        assert input('is the light bulb on? [Y/n] ') in ['y', 'Y', '']

    def assert_off():
        assert input('is the light bulb off? [Y/n] ') in ['y', 'Y', '']

    device = gosund.get_device(light_bulb_id)

    # start in off state
    assert_off()

    # turn on light bulb
    device.turn_on()
    assert_on()

    # turn off light bulb
    device.turn_off()
    assert_off()

    # flip the light bulb on
    device.switch()
    assert_on()

    # flip the light bulb off
    device.switch()
    assert_off()
