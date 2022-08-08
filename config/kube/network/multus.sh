#!/bin/bash





BRIDGE=br0

alias podman-pid="podman inspect --format '{{ .State.Pid }}' $@"

ip link add kube-int type veth peer name kube-ext
ip link set netns $(podman-pid minikube) dev kube-int
ip link set kube-ext up
brctl addif ${BRIDGE} kube-ext


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
        "subnet": "192.168.80.0/24",
        "rangeStart": "192.168.80.201",
        "rangeEnd": "192.168.80.225"
      }
    }'
EOF

