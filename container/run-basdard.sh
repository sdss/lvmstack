#!/usr/bin/bash -l

BASDARD_NAME=`basename ${BASDARD_CONFIG##*/} .conf`
test -n "$BASDARD_PORT" || BASDARD_PORT=`shuf -i 2000-65000 -n 1`
BASDARD_ADAPTER="[NAME=$BASDARD_NAME,PORT=$BASDARD_PORT]"


LVM_ROOT=$HOME
LVM_TAN_PATH=$(ls -1 -d ${LVM_ROOT}/lvm/lvmtan ${LVM_ROOT}/lvm 2> /dev/null)

echo $LVM_TAN_PATH

PATH=$LVM_TAN_PATH/scripts:$PATH

if [ $LVM_RMQ ]; then 
     RMQ_CONNECTION="[user=guest,password=guest,host=$LVM_RMQ,port=5672]"
else
     test -n "$RMQ_CONNECTION" && RMQ_CONNECTION="[user=guest,password=guest,host=localhost,port=5672]"
fi

INSROOT_ETC_PATH=$LVM_TAN_PATH/config:$INSROOT_ETC_PATH
echo $LVM_DEBUG
if [ $LVM_DEBUG ]; then 
    PYTHONPATH=$(ls -1 -d ${LVM_ROOT}/lvm/*/python ${LVM_ROOT}/lvmtan/python 2>/dev/null | tr "\n" ":")
fi
QT_PLUGIN_PATH=$LVM_TAN_PATH/config:$QT_PLUGIN_PATH

test -n "$BASDARD_UI" && BASDARD_UI=+UI=$BASDARD_UI

echo $BASDARD_NAME
echo $BASDARD_UI

test -n "${DISPLAY}" && (sleep 0.3 && niceQUI --XXX.CONFIG:Endpoint=${BASDARD_ADAPTER}${BASDARD_UI} --LOGGER.LEVEL=INFO) &

basdard --CONFIG=${BASDARD_CONFIG} --ADAPTER=${BASDARD_ADAPTER} --CLU.RABBITMQ.CONN:MapStringString=${RMQ_CONNECTION} --LOGGER.LEVEL=INFO

if [ $LVM_DEBUG ]; then 
   sleep INFINITY
fi
