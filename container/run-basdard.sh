#!/usr/bin/bash -l

BASDARD_NAME = `basename ${BASDARD_CONFIG##*/} .conf`
test -n "$BASDARD_PORT" && BASDARD_PORT = `shuf -i 2000-65000 -n 1`
BASDARD_ADAPTER = "[NAME=$BASDARD_NAME,PORT=$BASDARD_PORT]"

LVMT_PATH=/root/lvmt
PATH=$LVMT_PATH/scripts:$PATH

if [ $RMQ_HOST ]; then 
     RMQ_CONNECTION = "[user=guest,password=guest,host=$RMQ_HOST,port=5672]"
else
     test -n "$RMQ_CONNECTION" && RMQ_CONNECTION = "[user=guest,password=guest,host=localhost,port=5672]"
fi


INSROOT_ETC_PATH=$LVMT_PATH/config:$INSROOT_ETC_PATH
echo $TAN_DEBUG
if [ $TAN_DEBUG ]; then 
    PYTHONPATH=$LVMT_PATH/python/:$PYTHONPATH
fi
QT_PLUGIN_PATH=$LVMT_PATH/config:$QT_PLUGIN_PATH

test -n "$BASDARD_UI" && BASDARD_UI=+UI=$BASDARD_UI

echo $BASDARD_NAME
echo $BASDARD_UI

test -n "$DISPLAY" && (sleep 0.3 && niceQUI --XXX.CONFIG:Endpoint=$BASDARD_ADAPTER$BASDARD_UI --LOGGER.LEVEL=INFO) &

basdard --CONFIG=$BASDARD_CONFIG --ADAPTER=$BASDARD_ADAPTER --CLU.RABBITMQ.CONN:MapStringString=$RMQ_CONNECTION --LOGGER.LEVEL=INFO


