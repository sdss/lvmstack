#!/usr/bin/bash

PYTHON=/usr/bin/python3

# LVM_ACTOR # (Mandatory)

# LVM_RMQ_HOST #(Optional)
# LVM_ACTOR_ARGS # (Optional)
# LVM_DEBUG=true # (Optional)


LVM_ACTOR_CONFIG=${LVM_ACTOR_CONFIG:-${LVM_ACTOR}}



if [ ! $LVM_ACTOR_PATH ]; then 
  if [ $LVM_DEBUG ]; then 
    LVM_ACTOR_PATH=${HOME}/${LVM_ACTOR}/python/${LVM_ACTOR}
    export PYTHONPATH=${LVM_ACTOR_PATH}/python/:$PYTHONPATH
  else
    LVM_ACTOR_PATH=$(${PYTHON} -c "import ${LVM_ACTOR} as _; print(_.__path__[0])")
  fi
fi
echo $LVM_ACTOR_PATH

export LVMT_DATA_ROOT="${LVM_DATA_ROOT:=${HOME}/data}"

if [ $LVM_RMQ_HOST ]; then 
  sed "s/host: .*$/host: $LVM_RMQ_HOST/" < $LVM_ACTOR_PATH/etc/$LVM_ACTOR_CONFIG.yml \
            > $HOME/${LVM_ACTOR_CONFIG}_${LVM_RMQ_HOST}.yml
  LVM_ACTOR_CONFIG_ABS=$HOME/${LVM_ACTOR_CONFIG}_${LVM_RMQ_HOST}
else
  LVM_ACTOR_CONFIG_ABS=$LVM_ACTOR_PATH/etc/${LVM_ACTOR_CONFIG}
fi


${PYTHON} $LVM_ACTOR_PATH/__main__.py -c ${LVM_ACTOR_CONFIG_ABS}.yml ${LVM_ACTOR_ARGS} start --debug

if [ $LVM_DEBUG ]; then 
   sleep INFINITY
fi
