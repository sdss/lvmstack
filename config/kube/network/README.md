



# http://blog.oddbit.com/post/2014-08-11-four-ways-to-connect-a-docker/

[root@nicelab network-scripts]# cat ifcfg-br0
DEVICE=br0
NM_CONTROLLED="no"
TYPE=Bridge
IPADDR=192.168.80.1
NETMASK=255.255.255.0
BOOTPROTO=none
ONBOOT=yes
DELAY=0

[root@nicelab network-scripts]# cat ifcfg-eno2
DEVICE=eno2
NM_CONTROLLED="no"
HWADDR=b8:ca:3a:5f:1e:15
TYPE=Ethernet
BRIDGE=br0
BOOTPROTO=none
ONBOOT=yes
DELAY=10
