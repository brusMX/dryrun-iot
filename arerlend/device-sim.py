import os, time
import json
import sys
import iothub_client
from iothub_client import IoTHubClient, IoTHubClientError, IoTHubTransportProvider, IoTHubClientResult
from iothub_client import IoTHubMessage, IoTHubMessageDispositionResult, IoTHubError, DeviceMethodReturnValue

# String containing Hostname, Device Id & Device Key in the format
CONNECTION_STRING = os.environ["HubDeviceConnectionString"]
# choose HTTP, AMQP or MQTT as transport protocol
PROTOCOL = IoTHubTransportProvider.MQTT
MESSAGE_TIMEOUT = 10000
AVG_WIND_SPEED = 10.0
SEND_CALLBACKS = 0 

csv_path = "C:\\Users\\arerlend.REDMOND\\dev\\iotdryrun\\motor.csv"

def send_confirmation_callback(message, result, user_context):
    global SEND_CALLBACKS
    print ( "Confirmation[%d] received for message with result = %s" % (user_context, result) )
    map_properties = message.properties()
    print ( "    message_id: %s" % message.message_id )
    print ( "    correlation_id: %s" % message.correlation_id )
    key_value_pair = map_properties.get_internals()
    print ( "    Properties: %s" % key_value_pair )
    SEND_CALLBACKS += 1
    print ( "    Total calls confirmed: %d" % SEND_CALLBACKS )

def iothub_client_init():
    # prepare iothub client
    client = IoTHubClient(CONNECTION_STRING, PROTOCOL)
    # set the time until a message times out
    client.set_option("messageTimeout", MESSAGE_TIMEOUT)
    client.set_option("logtrace", 0)
    client.set_option("product_info", "HappyPath_Simulated-Python")
    return client

def iothub_client_telemetry_sample_run():

    try:
        client = iothub_client_init()
        print ( "IoT Hub device sending periodic messages, press Ctrl-C to exit" )
        message_counter = 0

        with open(csv_path,'r') as f:
            
            # get rid of header
            f.readline()
            
            while True:
                
                csv_batch_num = 0

                for line in f:
                    index, speed, torque, volts = line.strip().split(',')

                    guid = "batch_" + str(csv_batch_num) + "_row_" + index

                    msg = {}
                    msg['liftOperation'] = guid
                    msg['eventTime'] = time.strftime("%Y-%m-%d %H:%M:%S")
                    msg['speed'] = speed
                    msg['torque'] = torque
                    msg['volts'] = volts
                    
                    json_msg = json.dumps(msg)
                    
                    message = IoTHubMessage(json_msg)
                    
                    client.send_event_async(message, send_confirmation_callback, message_counter)
                    print ( "IoTHubClient.send_event_async accepted message [%s] for transmission to IoT Hub." % guid )
                    
                    status = client.get_send_status()
                    print status

                    time.sleep(1)

                
                # seek to start
                f.seek(0,0)

                # get rid of header
                f.readline()

                csv_batch_num += 1

                # sleep for 30 secs
                time.sleep(30)
            

    except IoTHubError as iothub_error:
        print ( "Unexpected error %s from IoTHub" % iothub_error )
        return
    except KeyboardInterrupt:
        print ( "IoTHubClient sample stopped" )

if __name__ == '__main__':
    print ( "Simulating a device using the Azure IoT Hub Device SDK for Python" )
    print ( "    Protocol %s" % PROTOCOL )
    print ( "    Connection string=%s" % CONNECTION_STRING )

    iothub_client_telemetry_sample_run()