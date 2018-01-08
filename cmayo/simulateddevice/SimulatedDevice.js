'use strict';

var clientFromConnectionString = require('azure-iot-device-mqtt').clientFromConnectionString;
var Message = require('azure-iot-device').Message;
var csv = require('fast-csv');
const uuidv1 = require('uuid/v1');

require('dotenv').config();

var connectionString = process.env.IOT_HUB_CONNECTION_STRING;

var client = clientFromConnectionString(connectionString);

var connectCallback = function (err) {
    if (err) {
        console.log('Could not connect: ' + err);
    } else {
        console.log('Client connected');

        let csvstream = csv.fromPath('motor.csv', { headers: true })
        .on("data", function (row) {

            csvstream.pause();

            var data = JSON.stringify(
                {
                    "liftOperation": `chainlift-cmayo-${uuidv1()}`,
                    "eventTime": new Date().toISOString().replace(/T/, ' ').replace(/\..+/, ''),
                    "speed": row.running_speed,
                    "torque": row.torque,
                    "volts": row.voltage
                }
            );

            console.log(data);

            var message = new Message(data);

            client.sendEvent(message, printResultFor('send'));

            setInterval(function(){
                csvstream.resume();
            }, 1000);
        })
        .on("end", function () {
            console.log("We are done!")
        })
        .on("error", function (error) {
            console.log(error)
        });
    }
};

client.open(connectCallback);

function printResultFor(op) {
    return function printResult(err, res) {
        if (err) console.log(op + ' error: ' + err.toString());
        if (res) console.log(op + ' status: ' + res.constructor.name);
    };
}