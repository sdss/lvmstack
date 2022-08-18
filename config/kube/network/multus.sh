#!/bin/bash

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

