'use strict';

var iothub = require('azure-iothub');
require('dotenv').config();

var connectionString = process.env.IOT_HUB_CONNECTION_STRING;

var registry = iothub.Registry.fromConnectionString(connectionString);

var device = {
    deviceId: 'chainlift-cmayo'
}

registry.create(device, function(err, deviceInfo, res) {
    if (err) {
        registry.get(device.deviceId, printDeviceInfo);
    }

    if (deviceInfo) {
        printDeviceInfo(err, deviceInfo, res)
    }
});
  
function printDeviceInfo(err, deviceInfo, res) {
    if (deviceInfo) {
        console.log('Device ID: ' + deviceInfo.deviceId);
        console.log('Device key: ' + deviceInfo.authentication.symmetricKey.primaryKey);
    }
}