# Quickstart
The following chapter "Install minikube & kubectl" describes only the installation on linux.
Minikube can also be used on Mac & Windows with docker or a virtual machine (eg: vmware), see details [here](https://minikube.sigs.k8s.io/docs/start/). 
The deployment of the lvm containers should then also work.

# Install minikube & kubectl
## Install minikube

    curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
    sudo install minikube-linux-amd64 /usr/local/bin/minikube
    minikube version

## Installing Kubectl

    curl -LO https://storage.googleapis.com/kubernetes-release/release/`curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt`/bin/linux/amd64/kubectl
    sudo install kubectl /usr/local/bin/

## Choose podman or docker for minikube
For minikube a container or virtual machine has to be selected, before proceeding choose podman or docker, one of them has to be installed beforehand.

### Podman only: add passwordless sudo

    USER_SUDO_FILE=/etc/sudoers.d/$USER;  echo "$USER ALL=(ALL) NOPASSWD: /usr/bin/podman" | sudo tee -a $USER_SUDO_FILE > /dev/null
    minikube config set driver podman
    minikube config set container-runtime cri-o

### Docker only: add docker group

    sudo usermod -aG docker $USER && newgrp docker

# Deployment 

## Download all the necessary files for lvm from github:

    git clone https://github.com/sdss/lvm.git
    cd lvm
    
    # Define LVM root
    export LVM_ROOT=$PWD

    # for now we do store persistent data here:
    mkdir -p ${LVM_ROOT}/var/data && chmod 777 ${LVM_ROOT}/var/data
    mkdir -p ${LVM_ROOT}/var/jupyter && chmod 777 ${LVM_ROOT}/var/jupyter
    mkdir -p ${LVM_ROOT}/var/rabbitmq && chmod 777 ${LVM_ROOT}/var/rabbitmq

## Start minikube

    # check memory and cpu numbers
    minikube start --mount --mount-string="$LVM_ROOT:/lvm" --extra-config=kubelet.housekeeping-interval=10s --memory 16384 --cpus=2 
 
    minikube status 

    minikube addons enable metrics-server
    minikube addons enable dashboard
    minikube addons list

    minikube ip
    
    # optional dashboard
    minikube dashboard --url&
    kubectl proxy&
    # http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/http:kubernetes-dashboard:/proxy/#/pod?namespace=default

## Start rabbitmq

    # rabbitmq: http://192.168.49.2:8081
    kubectl create -f $LVM_ROOT/config/kube/rabbitmq.yaml

Check address 192.168.49.2 with 'minikube ip', before proceeding, please check that rabbitmq dashboard is reachable.

## Build containers into minikube

    minikube image build --tag localhost/lvm_actor ${LVM_ROOT}/config/container/actor/
    minikube image build --tag localhost/lvm_jupyter ${LVM_ROOT}/config/container/jupyter/
    minikube image ls
    minikube image rm localhost/lvm_actor:latest

    # minikube image build --tag localhost/lvm_actor:$(date +"%y%m%d") ${LVM_ROOT}/config/container/actor/

## Start lvm containers   

    # jupyter: http://192.168.49.2:8082
    kubectl create -f $LVM_ROOT/config/kube/lvm_jupyter.yaml

    kubectl create -f $LVM_ROOT/config/kube/lvm_moe-sim.yaml 

    # lvmscraper: http://192.168.49.2:8085/
    kubectl create -f $LVM_ROOT/config/kube/lvm_scraper.yaml

    kubectl create -f $LVM_ROOT/config/kube/lvm_nps-sim.yaml
     
    kubectl create -f $LVM_ROOT/config/kube/lvm_ieb.yaml
    kubectl create -f $LVM_ROOT/config/kube/lvm_ecp.yaml
    kubectl create -f $LVM_ROOT/config/kube/lvm_scp.yaml # fails

    kubectl create -f $LVM_ROOT/config/kube/lvm_sci_pwi-sim.yaml
    kubectl create -f $LVM_ROOT/config/kube/lvm_skyw_pwi-sim.yaml
    kubectl create -f $LVM_ROOT/config/kube/lvm_skye_pwi-sim.yaml
    kubectl create -f $LVM_ROOT/config/kube/lvm_spec_pwi-sim.yaml

    kubectl create -f $LVM_ROOT/config/kube/lvm_sci_agcam-sim.yaml
    kubectl create -f $LVM_ROOT/config/kube/lvm_skyw_agcam-sim.yaml
    kubectl create -f $LVM_ROOT/config/kube/lvm_skye_agcam-sim.yaml
    kubectl create -f $LVM_ROOT/config/kube/lvm_spec_agcam-sim.yaml

    kubectl create -f $LVM_ROOT/config/kube/lvm_sci_agp.yaml
    kubectl create -f $LVM_ROOT/config/kube/lvm_skyw_agp.yaml
    kubectl create -f $LVM_ROOT/config/kube/lvm_skye_agp.yaml
    kubectl create -f $LVM_ROOT/config/kube/lvm_spec_agp.yaml

## Test UIs

    vncviewer $(minikube ip):1
    vncviewer $(minikube ip):2
    vncviewer $(minikube ip):3
    vncviewer $(minikube ip):4
    niceQUI --MOE.CONFIG:Endpoint=[NAME=lvm.moe-sim,HOST=$(minikube ip),PORT=40000]+UI=$LVM_ROOT/lvmtan/config/lvm/lvm.all.ui 
    python3.9 $LVM_ROOT/wasndas/lvmcam/utils/simple_camui.py -c lvm.sci.agcam -k lvm.sci.km -t lvm.sci.pwi -H $(minikube ip)

## Stopping containers

    kubectl delete pod lvm-moe-sim

    kubectl delete pod lvm-sci-pwi-sim # optional --grace-period=0  --force

    kubectl delete -n default pod lvm-skyw-pwi-sim

## Exec commands in pod

    kubectl exec -ti lvm-sci-pwi-sim -- bash -l

## Access minikube container

    minikube ssh -- bash -l 
    minikube ssh -- sudo podman images
    # or
    sudo podman exec -ti minikube podman images


# TODO
* https://kubernetes.io/docs/concepts/configuration/configmap/

# NOTES
* https://jamesdefabia.github.io/docs/user-guide/kubectl-cheatsheet/
* https://minikube.sigs.k8s.io/docs/handbook/pushing/
* https://github.com/flannel-io/flannel/blob/master/Documentation/kube-flannel.yml
* https://github.com/kvaps/bridget/
