#!/bin/bash
#Lets get the keys to the kingdom
source .env
export IOT_CON_STRING=`az iot hub show-connection-string -n $IOT_HUB_NAME -g $RESOURCE_GROUP -o tsv`
export RAND_SUFIX=$(cat /dev/urandom | env LC_CTYPE=C tr -dc 'a-z0-9' | fold -w 4 | head -n 1)
export SENSOR_ID=bruno-${RAND_SUFIX}
az iot device create -d $SENSOR_ID --hub-name $IOT_HUB_NAME -g $RESOURCE_GROUP
export SENSOR_CS=$(az iot device show-connection-string -d $SENSOR_ID --hub-name $IOT_HUB_NAME -g $RESOURCE_GROUP -o tsv)
echo "SENSOR_CS says:"
echo $SENSOR_CS
# Now you can deploy your simulated device with that connection string
