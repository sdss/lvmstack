#!/usr/bin/bash

PYTHON=/usr/bin/python3

# LVM_ACTOR # (Mandatory)

# LVM_RMQ_HOST #(Mandatory for kubernetes)
# LVM_ACTOR_ARGS # (Optional)
# LVM_DEBUG=true # (Optional)

LVM_ACTOR_CONFIG=${LVM_ACTOR_CONFIG:-${LVM_ACTOR}}
LVM_ROOT=$HOME

if [ $LVM_DEBUG ]; then 
  LVM_ACTOR_PATH=$(ls -1 -d ${LVM_ROOT}/lvm/${LVM_ACTOR} ${LVM_ACTOR} 2> /dev/null)/python/${LVM_ACTOR}
  export PYTHONPATH=$(ls -1 -d ${LVM_ROOT}/lvm/*/python ${LVM_ROOT}/${LVM_ACTOR}/python 2>/dev/null | tr "\n" ":")
else
  LVM_ACTOR_PATH=$(${PYTHON} -c "import ${LVM_ACTOR} as _; print(_.__path__[0])")
fi
#echo $LVM_ACTOR_PATH
#echo $PYTHONPATH

export LVMT_DATA_ROOT="${LVM_DATA_ROOT:=/data}"

if [ $LVM_RMQ_HOST ]; then 
  LVM_ACTOR_CONFIG_ABS=$LVM_ACTOR_PATH/etc/${LVM_ACTOR_CONFIG}_${LVM_RMQ_HOST}
  sed "s/host: .*$/host: $LVM_RMQ_HOST/" < $LVM_ACTOR_PATH/etc/$LVM_ACTOR_CONFIG.yml \
            > ${LVM_ACTOR_CONFIG_ABS}.yml
  
else
  LVM_ACTOR_CONFIG_ABS=$LVM_ACTOR_PATH/etc/${LVM_ACTOR_CONFIG}
fi

echo "Using config: $LVM_ACTOR_CONFIG_ABS"
${PYTHON} $LVM_ACTOR_PATH/__main__.py -c ${LVM_ACTOR_CONFIG_ABS}.yml ${LVM_ACTOR_ARGS} start --debug

#trap : TERM INT; ${PYTHON} $LVM_ACTOR_PATH/__main__.py -c ${LVM_ACTOR_CONFIG_ABS}.yml ${LVM_ACTOR_ARGS} start --debug  & wait"]

if [ $LVM_DEBUG ]; then 
   sleep INFINITY
fi
