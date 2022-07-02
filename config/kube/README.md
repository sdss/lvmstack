# Install Minikube & kubectl

This chapter is only for installation on linux, Minikube can also be used on Mac & Windows with docker or a virtual machine (eg: vmware),
see details [here](https://minikube.sigs.k8s.io/docs/start/). The deployment of the lvm containers should then also work.

# Quickstart Linux

## Install minikube

    curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
    sudo install minikube-linux-amd64 /usr/local/bin/minikube
    minikube version

## Installing Kubectl

    curl -LO https://storage.googleapis.com/kubernetes-release/release/`curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt`/bin/linux/amd64/kubectl
    sudo install kubectl /usr/local/bin/
## Choose podman or docker
For minikube a container or virtual machine has to be select, in the following sub chapters choose one of them. Podman or Docker has to be installed beforehand.

### Add passwordless sudo for podman

    USER_SUDO_FILE=/etc/sudoers.d/$USER;  echo "$USER ALL=(ALL) NOPASSWD: /usr/bin/podman" | sudo tee -a $USER_SUDO_FILE > /dev/null

###  Add  docker group

    sudo usermod -aG docker $USER && newgrp docker
    

# Download all the necessary files for lvm from github:

    git clone https://github.com/sdss/lvm.git
    cd lvm

    # for now we do store persistent data here:
    mkdir -p var/data && chmod 777 var/data
    mkdir -p var/jupyter && chmod 777 var/jupyter
    mkdir -p var/rabbitmq && chmod 777 var/rabbitmq


# Start minikube

## Define LVM root
    export LVM_ROOT=$PWD

### Setting podman as minikube container

    minikube config set driver podman
    minikube config set container-runtime cri-o

## Configure minikube

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

### The dashboard can be accessed with this link:
    http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/http:kubernetes-dashboard:/proxy/#/pod?namespace=default



## Start rabbitmq

     kubectl create -f $LVM_ROOT/config/kube/rabbitmq.yaml

### Access rabbitmq dasboard

     http://192.168.49.2:8081



## Start lvm actor & services
Before starting please check that rabbitmq dashboard is reachable.

     kubectl create -f $LVM_ROOT/config/kube/lvm_moe-sim.yaml 

# minikube image build --tag localhost/lvm_actor:$(date +"%y%m%d") ${LVM_ROOT}/config/container/actor/
minikube image build --tag localhost/lvm_actor ${LVM_ROOT}/config/container/actor/

minikube image build --tag localhost/lvm_jupyter /home/briegel/workspace/lvm/config/container/jupyter/
minikube image ls

kubectl create -f $LVM_ROOT/config/kube/lvm_scraper.yaml
kubectl create -f $LVM_ROOT/config/kube/lvm_nps-sim.yaml

kubectl create -f $LVM_ROOT/config/kube/lvm_sci_pwi-sim.yaml
kubectl create -f $LVM_ROOT/config/kube/lvm_skyw_pwi-sim.yaml
kubectl create -f $LVM_ROOT/config/kube/lvm_skye_pwi-sim.yaml
kubectl create -f $LVM_ROOT/config/kube/lvm_spec_pwi-sim.yaml

vncviewer $(minikube ip):1
vncviewer $(minikube ip):2
vncviewer $(minikube ip):3
vncviewer $(minikube ip):4

kubectl create -f $LVM_ROOT/config/kube/lvm_sci_agcam-sim.yaml
kubectl create -f $LVM_ROOT/config/kube/lvm_skyw_agcam-sim.yaml
kubectl create -f $LVM_ROOT/config/kube/lvm_skye_agcam-sim.yaml
kubectl create -f $LVM_ROOT/config/kube/lvm_spec_agcam-sim.yaml

kubectl create -f $LVM_ROOT/config/kube/lvm_sci_agp.yaml
kubectl create -f $LVM_ROOT/config/kube/lvm_skyw_agp.yaml
kubectl create -f $LVM_ROOT/config/kube/lvm_skye_agp.yaml
kubectl create -f $LVM_ROOT/config/kube/lvm_spec_agp.yaml

kubectl create -f $LVM_ROOT/config/kube/lvm_jupyter.yaml

niceQUI --MOE.CONFIG:Endpoint=[NAME=lvm.moe-sim,HOST=$(minikube ip),PORT=40000]+UI=$LVM_ROOT/lvmtan/config/lvm/lvm.all.ui 
python3.9 $LVM_ROOT/wasndas/lvmcam/utils/simple_camui.py -c lvm.sci.agcam -k lvm.sci.km -t lvm.sci.pwi -H $(minikube ip)

# rabbitmq: http://192.168.49.2:8081
# jupyter: http://192.168.49.2:8082
# lvmscraper: http://192.168.49.2:8085/

kubectl delete -n default pod lvm_moe-sim&

# https://cloud.google.com/blog/products/containers-kubernetes/kubernetes-best-practices-terminating-with-grace
# https://kubernetes.io/docs/tasks/run-application/force-delete-stateful-set-pod/#force-deletion

kubectl delete -n default pod lvm-sci-pwi-sim # optional --grace-period=0  --force
kubectl delete -n default pod lvm-skyw-pwi-sim
kubectl delete -n default pod lvm-skye-pwi-sim
kubectl delete -n default pod lvm-spec-pwi-sim
kubectl delete pod lvm-scraper



kubectl exec -ti lvm-sci-pwi-sim -- bash -l



apt update
apt install -y iputils-ping iproute2



ip route add 10.96.0.0/12 via $(minikube ip) # svc
ip route add 172.17.0.0/16 via $(minikube ip) # pods

kubectl create -f config/kube/kube-flannel.yml
kubectl apply -f /usr/share/k8s-yaml/multus/multus.yaml

# https://jamesdefabia.github.io/docs/user-guide/kubectl-cheatsheet/
# https://minikube.sigs.k8s.io/docs/handbook/pushing/

# access minikube container
minikube ssh -- sudo podman images
# or
sudo podman exec -ti minikube podman images




# external 
# minikube addons enable registry
# minikube image push 192.168.49.2:5000/lvm_actor



kubectl get pod,svc -n default
kubectl create -f config/kube/lvm_sci_pwi-sim.yaml
kubectl exec lvm-sci-pwi-sim -- capsh --print

kubectl exec -ti lvm-nps-sim -- bash -l


# TODO

https://kubernetes.io/docs/concepts/configuration/configmap/


# https://github.com/flannel-io/flannel/blob/master/Documentation/kube-flannel.yml
kubectl get psp
kubectl create -f config/kube/lvm_sci_pwi-sim.yaml

https://github.com/kvaps/bridget/

kubectl apply -f https://raw.githubusercontent.com/k8snetworkplumbingwg/multus-cni/master/deployments/multus-daemonset-thick-plugin.yml
