# LVM container for actors - to rule them all¹

- Needs some enviroment variables in the kube files or as container -e parameters
- Supports two modes.
  - running only with pypi installed packages (code & config) from container build.
  - in debug mode with mounted host file system develop directories.

### LVM_ACTOR - name your actor
Its mandatory to provide the actor python module name

### LVM_RMQ_HOST: hostname for rabbitmq
Replaces the rmq host address with $LVM_RMQ_HOST

    actor:
       ...
       host: localhost
       ...

### LVM_ACTOR_ARGS # (Optional)
Add some options to actor startup
### LVM_DEBUG=yes # (Optional)


# Quickstart

# Install minikube & kubectl
## Install minikube

# TODO


# NOTES

¹ Except lvmtan & lvmpwi
