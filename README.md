# gosundpy

[![PyPI version](https://badge.fury.io/py/gosundpy.svg)](https://badge.fury.io/py/gosundpy)

Control your Gosund smart devices via python code.

## Install

```bash
pip install gosundpy
```

## Prerequisites

In order to control your devices, you must register your devices using the Tuya
Smart app ([ios][1]/[android][2]) and create a new Cloud Project in the Tuya
IoT Platform.

## Usage

```python
import time

from gosundpy import Gosund

gosund = Gosund('username', 'password', 'access_id', 'access_key')

commands = ['turn_off', 'turn_on', 'turn_off', 'switch', 'switch', 'turn_off']

switch = gosund.get_device('12345')
for cmd in commands:
    getattr(switch, cmd)()
    time.sleep(1)

lightbulb = gosund.get_device('67890')
for cmd in commands:
    getattr(lightbulb, cmd)()
    time.sleep(1)
```

<!-- links -->
[1]: https://apps.apple.com/us/app/tuya-smart/id1034649547
[2]: https://play.google.com/store/apps/details?id=com.tuya.smart&hl=en_US&gl=US
