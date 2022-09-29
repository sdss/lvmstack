# Create bridge to ethernet if
[Four ways to connect a docker](http://blog.oddbit.com/post/2014-08-11-four-ways-to-connect-a-docker/)

## CentOS

### /etc/sysconfig/network-scripts/ifcfg-br-eno2
    DEVICE=br-eno2
    NM_CONTROLLED="no"
    TYPE=Bridge
    IPADDR=192.168.80.1
    NETMASK=255.255.255.0
    BOOTPROTO=none
    ONBOOT=yes
    DELAY=0

### /etc/sysconfig/network-scripts/ifcfg-eno2
    DEVICE=eno2
    NM_CONTROLLED="no"
    HWADDR=b8:ca:3a:5f:1e:15
    TYPE=Ethernet
    BRIDGE=br-eno2
    BOOTPROTO=none
    ONBOOT=yes
    DELAY=10
