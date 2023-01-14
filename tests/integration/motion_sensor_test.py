def test_motion_sensor(gosund, motion_id):

    device = gosund.get_device(motion_id)

    val = device.motion_sensed()
    assert input(f'is the motion sensed state currently {val}? [Y/n] ') in ['y', 'Y', '']
