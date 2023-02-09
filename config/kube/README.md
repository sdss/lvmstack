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

    git clone --recurse-submodules -j8 --remote-submodules https://github.com/sdss/lvm.git
    cd lvm
    
    # Define LVM root - IMPORTANT: this will be mounted into the container !
    export LVM_ROOT=$PWD

    # for now we do store persistent data here:
    mkdir -p ${LVM_ROOT}/var/data && chmod 777 ${LVM_ROOT}/var/data
    mkdir -p ${LVM_ROOT}/var/jupyter/work && chmod 777 ${LVM_ROOT}/var/jupyter/work
    mkdir -p ${LVM_ROOT}/var/jupyter/python && chmod 777 ${LVM_ROOT}/var/jupyter/python
    mkdir -p ${LVM_ROOT}/var/rabbitmq && chmod 777 ${LVM_ROOT}/var/rabbitmq

## Start minikube

    # check memory and cpu numbers
    minikube config set memory 16384
    minikube config set cpus 2
    
    minikube start --mount --mount-string="$LVM_ROOT:/lvm" --extra-config=kubelet.housekeeping-interval=10s

    # minikube start --mount --mount-string="$LVM_ROOT:/lvm" --extra-config=kubelet.housekeeping-interval=10s --memory=16384 --cpus=2 
 
    minikube status 

    # check that /lvm is mounted correctly !
    minikube ssh -- ls -l /lvm

    minikube addons enable metrics-server
    minikube addons enable dashboard
    minikube addons list

    minikube ip
    
    ## optional dashboard
    # minikube dashboard --url&
    kubectl create -f $LVM_ROOT/config/kube/extra/minikube-dashboard.yaml

    kubectl proxy --address 0.0.0.0 --accept-hosts '.*' &
    # http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/http:kubernetes-dashboard:/proxy/#/pod?namespace=default

   

## prerequisits for GigE ag cameras (Optional)

    # check script if the network interface and ip net is correct
    sudo $LVM_ROOT/config/config/kube/network/extraif.sh
    $LVM_ROOT/config/config/kube/network/multus.sh

## Creating namespaces

    kubectl apply -f $LVM_ROOT/config/kube/namespace/lvm_sys-ns.yaml
    # kubectl apply -f $LVM_ROOT/config/kube/namespace/lvm_ics-ns.yaml
    kubectl get namespaces
    
    # define default namespace   
    # kubectl config set-context $(kubectl config current-context) --namespace=lvm-ics
    
## Start rabbitmq

    # rabbitmq: http://192.168.49.2:8081
    kubectl create -n lvm-sys -f $LVM_ROOT/config/kube/rabbitmq.yaml


## Build containers into minikube (optional)

    # containers for lvmjupyter and lvmactor are on github

    # https://minikube.sigs.k8s.io/docs/commands/image/#minikube-image-build
    # https://minikube.sigs.k8s.io/docs/handbook/pushing/

    # minikube image build --tag localhost/lvmactor ${LVM_ROOT}/config/container/actor/
    # alternative build & push
    # podman build --tag localhost/lvmactor -f ${LVM_ROOT}/config/container/actor/Dockerfile ${LVM_ROOT}/config/container/actor/
    # podman save localhost/lvmactor:latest -o localhost_lvmactor_latest.img
    # minikube image load localhost_lvmactor_latest.img
    
    # minikube image build --tag localhost/lvmjupyter ${LVM_ROOT}/config/container/jupyter/
    # podman build --tag localhost/lvmjupyter -f ${LVM_ROOT}/config/container/jupyter/Dockerfile ${LVM_ROOT}/config/container/jupyter
    # podman save localhost/lvmjupyter:latest -o localhost_lvmjupyter_latest.img
    # minikube image load localhost_lvmjupyter_latest.img

    # minikube image ls | grep localhost

    # minikube image build --tag localhost/lvmactor:$(date +"%y%m%d") ${LVM_ROOT}/config/container/actor/

    # minikube image rm localhost/lvmactor:latest

## Start lvm containers in simulation

    # Check address 192.168.49.2 with 'minikube ip', before proceeding, please check that rabbitmq dashboard is reachable.

    # jupyter: http://192.168.49.2:8082
    kubectl create -n lvm-sys -f $LVM_ROOT/config/kube/lvm-jupyter.yaml

    # lvmscraper: http://192.168.49.2:8085/
    # kubectl create -n lvm-sys -f $LVM_ROOT/config/kube/lvm-scraper.yaml

    kubectl create -f $LVM_ROOT/config/kube/lvm-moe-sim.yaml 

    kubectl create -f $LVM_ROOT/config/kube/lvm-nps-sim.yaml

    kubectl create -f $LVM_ROOT/config/kube/lvm-ieb.yaml
    kubectl create -f $LVM_ROOT/config/kube/lvm-ecp.yaml
    kubectl create -f $LVM_ROOT/config/kube/lvm-scp.yaml # fails

    kubectl create -f $LVM_ROOT/config/kube/lvm-sci-pwi-sim.yaml
    kubectl create -f $LVM_ROOT/config/kube/lvm-skyw-pwi-sim.yaml
    kubectl create -f $LVM_ROOT/config/kube/lvm-skye-pwi-sim.yaml
    kubectl create -f $LVM_ROOT/config/kube/lvm-spec-pwi-sim.yaml

    kubectl create -f $LVM_ROOT/config/kube/lvm-sci-ag-sim.yaml
    kubectl create -f $LVM_ROOT/config/kube/lvm-skyw-ag-sim.yaml
    kubectl create -f $LVM_ROOT/config/kube/lvm-skye-ag-sim.yaml
    kubectl create -f $LVM_ROOT/config/kube/lvm-spec-ag-sim.yaml


## Start lvm containers with real hardware (Optional)

    kubectl delete pod lvm-spec-ag-sim
    kubectl create -f $LVM_ROOT/config/kube/lvm-spec-ag.yaml

    # kubectl create -f $LVM_ROOT/config/kube/lvm-spec-agcam.yaml


## Test UIs

    # PWI4 UI
    vncviewer $(minikube ip):1 &
    vncviewer $(minikube ip):2 &

    vncviewer $(minikube ip):3 &
    vncviewer $(minikube ip):4 &

    # Simple lvmcam UI sci
    python3.9 $LVM_ROOT/lvmcam/utils/simple_camui.py -c lvm.sci.agcam -k lvm.sci.km -t lvm.sci.pwi -H $(minikube ip)

    # TwiceAsNice motor UI
    vncviewer $(minikube ip):5 &
    # TwiceAsNice has to be installed.
    # niceQUI --MOE.CONFIG:Endpoint=[NAME=lvm.moe-sim,HOST=$(minikube ip),PORT=40000]+UI=$LVM_ROOT/lvmtan/config/lvm/lvm.all.ui &

## Stopping containers

    kubectl delete pod lvm-moe-sim

    kubectl delete pod lvm-sci-pwi-sim # optional --grace-period=0  --force

    kubectl delete -n default pod lvm-skyw-pwi-sim
    
    kubectl delete all --all -n default


## Exec commands into container

    kubectl exec -ti lvm-sci-pwi-sim -- bash -l
    
    # pod with multiple containers
    kubectl exec -ti lvm-sci-ag-sim -c lvm-sci-agp -- bash -l
    
    kubectl exec -ti -n lvm-sys lvm-jupyter -- bash -l


## Access minikube container

    minikube ssh -- bash -l 
    minikube ssh -- sudo podman images
    # or sudo podman exec -ti minikube podman images
    
## Accesing logs of containers

    kubectl logs lvm-moe-sim
    # continuously watching
    kubectl logs -f lvm-sci-ag-sim -c lvm-sci-agp

## Got lost ?

    minikube delete
    
    
# TODO
- https://kubernetes.io/docs/concepts/configuration/configmap/
- https://stackoverflow.com/questions/47128586/how-to-delete-all-resources-from-kubernetes-one-time

# NOTES
- https://jamesdefabia.github.io/docs/user-guide/kubectl-cheatsheet/
- https://minikube.sigs.k8s.io/docs/handbook/pushing/
- https://github.com/flannel-io/flannel/blob/master/Documentation/kube-flannel.yml
- https://github.com/kvaps/bridget/
