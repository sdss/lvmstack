# LVM container for actors - to rule them all¹

- Needs some enviroment variables in the kube files or as container -e parameters
- Supports two modes.
  - running only with pypi installed packages (code & config) from container build.
  - in debug mode with mounted host file system develop directories.

### LVM_ACTOR - name your actor
Its mandatory to provide the actor python module name

### LVM_RMQ_HOST: hostname for rabbitmq
Replaces the usual rmq localhost host address with $LVM_RMQ_HOST

    actor:
       ...
       host: localhost
       ...
### LVM_ACTOR_CONFIG
Name the config file, if it is not named as the actor python module name.

### LVM_ACTOR_ARGS
Add some options to actor startup

### LVM_DEBUG=yes


# TODO

# NOTES

¹ Except lvmtan & lvmpwi
