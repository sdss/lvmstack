# LVM container for actors - to rule them all¹

- It needs some enviroment variables in the kube files or as container -e parameters
- It supports two modes.
  - running only with pypi installed packages (code & config) from container build
  - in debug mode with mounted host file systems packages

### LVM_ACTOR - name your actor (MANDATORY)

### LVM_RMQ_HOST: hostname for rabbitmq (Mandatory for kubernetes)
 This will
### LVM_ACTOR_ARGS # (Optional)
### LVM_DEBUG=yes # (Optional)


# Quickstart

# Install minikube & kubectl
## Install minikube

# TODO


# NOTES

¹ Except lvmtan & lvmpwi
