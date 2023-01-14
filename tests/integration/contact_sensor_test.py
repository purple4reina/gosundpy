def test_contact_sensor(gosund, contact_id):

    device = gosund.get_device(contact_id)

    open = device.is_open()
    assert input(f'is the contact state currently open={open}? [Y/n] ') in ['y', 'Y', '']
