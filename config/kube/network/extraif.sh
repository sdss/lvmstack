#!/bin/bash

NET_DEV=eno2
NET_BRIDGE=br-${NET_DEV}
NET_ADDR=192.168.80
NET_MASK=24

brctl addbr ${NET_BRIDGE}
ip link set ${NET_BRIDGE} up
brctl addif ${NET_BRIDGE} ${NET_DEV}
ip addr del ${NET_ADDR}.0/${NET_MASK} dev ${NET_DEV}
ip addr add ${NET_ADDR}.0/${NET_MASK} dev ${NET_BRIDGE}

alias podman-pid="podman inspect --format '{{ .State.Pid }}' $@"

ip link add kube-int type veth peer name kube-ext
ip link set netns $(podman-pid minikube) dev kube-int
ip link set kube-ext up
brctl addif ${NET_BRIDGE} kube-ext
podman exec  -ti minikube ip link set kube-int

