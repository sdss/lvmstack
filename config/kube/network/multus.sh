#!/bin/bash

kubectl create -f $LVM_ROOT/config/kube/network/multus-daemonset-thick.yml
#kubectl apply -f https://raw.githubusercontent.com/k8snetworkplumbingwg/multus-cni/master/deployments/multus-daemonset-thick.yml


. $LVM_ROOT/config/kube/network/multus-config.sh

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
        "rangeStart": "${NET_ADDR}.126",
        "rangeEnd": "${NET_ADDR}.130"
      }
    }'
EOF

