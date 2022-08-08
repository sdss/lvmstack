#!/bin/bash

NET_DEV=eno2
NET_BRIDGE=br-${NET_DEV}
NET_ADDR=192.168.80
NET_MASK=24

# If the system wasnt setup on boot with the bridge
#
# brctl addbr ${NET_BRIDGE}
# ip link set ${NET_BRIDGE} up
# brctl addif ${NET_BRIDGE} ${NET_DEV}
# ip addr del ${NET_ADDR}.0/${NET_MASK} dev ${NET_DEV}
# ip addr add ${NET_ADDR}.0/${NET_MASK} dev ${NET_BRIDGE}


alias podman-pid="podman inspect --format '{{ .State.Pid }}' $@"

ip link add kube-int type veth peer name kube-ext
ip link set netns $(podman-pid minikube) dev kube-int
ip link set kube-ext up
brctl addif ${NET_BRIDGE} kube-ext


kubectl apply -f https://raw.githubusercontent.com/k8snetworkplumbingwg/multus-cni/master/deployments/multus-daemonset-thick-plugin.yml


cat <<EOF | kubectl create -f -
apiVersion: "k8s.cni.cncf.io/v1"
kind: NetworkAttachmentDefinition
metadata:
  name: ipvlan-def
spec:
  config: '{
      "cniVersion": "0.3.1",
      "type": "ipvlan",
      "master": "kube-int",
      "mode": "l2",
      "ipam": {
        "type": "host-local",
        "subnet": "${NET_ADDR}.0/${NET_MASK}",
        "rangeStart": "${NET_ADDR}.201",
        "rangeEnd": "${NET_ADDR}.225"
      }
    }'
EOF

