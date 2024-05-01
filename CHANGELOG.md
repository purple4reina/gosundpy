# CHANGELOG

## 0.9.0
### Features
+ Support for querying more than 20 devices at once.

## 0.8.0
### Features
+ Throw `GosundDeviceOfflineException` when sending a command fails because it
  is offline. This is a subclass of the `GosundException` class that used to be
  raised in this scenario.

## 0.7.0
### Features
+ Add optional timeout to all Tuya API calls

## 0.6.2
### Bug Fixes
+ Make caching of `Gosund.get_device_statuses` optional via opt in and
  configurable

## 0.6.1
### Bug Fixes
+ Re-add `GosundDevice.get_status` method

## 0.6.0
### Features
+ Reduce the number of Tuya API calls by getting status of all devices at once.
+ Calling `get_status` on a device now attempts to cache the status for 60
  seconds.  This cache is cleared any time a new device is looked up or
  `send_commands` is called.

## 0.5.1
### Bug Fixes
+ Improve release script for updating this CHANGELOG

## 0.5.0
### Features
+ Added motion sensor device
+ Added contact sensor device
+ Added light sensor device

## 0.4.0
### Features
+ Added temperature and humidity sensor devices

## 0.3.0
### Features
+ Added improved logging

## 0.2.0
### Features
+ Turn light bulbs on/off
### Bug Fixes
+ Fixed issue preventing proper installation via pip
