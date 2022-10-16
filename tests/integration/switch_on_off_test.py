def test_switch_on_off(gosund, switch_id):

    def assert_on():
        assert input('is the switch on? [Y/n] ') in ['y', 'Y', '']

    def assert_off():
        assert input('is the switch off? [Y/n] ') in ['y', 'Y', '']

    device = gosund.get_device(switch_id)

    # start in off state
    assert_off()

    # turn on switch
    device.turn_on()
    assert_on()

    # turn off switch
    device.turn_off()
    assert_off()

    # flip the switch on
    device.switch()
    assert_on()

    # flip the switch off
    device.switch()
    assert_off()
