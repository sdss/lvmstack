# LVM container for actors - to rule them all¹

- Needs some enviroment variables in the kube files or as container -e parameters
- Supports two modes.
  - running only with pypi installed packages (code & config) from container build.
  - in debug mode with mounted host file system develop directories.

### LVM_ACTOR - name your actor
Its mandatory to provide the actor python module name, it will start with default config of the same name from python/YOUR_ACTOR/etc/YOUR_ACTOR.yml

### LVM_RMQ_HOST: hostname for rabbitmq
Replaces the usual rmq localhost host address with $LVM_RMQ_HOST

    actor:
       ...
       host: localhost
       ...

### LVM_ACTOR_CONFIG
Name the config file (without '.yml'), if it is not named as the actor python module name.

### LVM_ACTOR_ARGS
Add some options to actor startup, eg --verbose or --simulate

### LVM_DEBUG=yes


# TODO

# NOTES

¹ Except lvmtan & lvmpwi
