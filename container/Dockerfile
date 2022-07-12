FROM ubuntu:20.04

## Get some karma ##
MAINTAINER Florian Briegel, briegel@mpia.de

# podman  build --tag ubuntu_lvm_tan --rm lvm_tan

# podman run -ti --rm --name lvm_tan -e DISPLAY --network=host --ipc=host --device /dev/dri -v ~/.Xauthority:/root/.Xauthority:Z -v .:/root/lvmt:Z -P localhost/ubuntu_lvm_tan

RUN apt update -y && \
    apt install -y wget && \
    echo "8\n7\n" | apt install -y software-properties-common && \
    echo "30\n1\n" | apt install -y keyboard-configuration && \
    wget -qO - https://zeroc.com/download/GPG-KEY-zeroc-release-B6391CB2CFBA643D | apt-key add - && \
    apt-add-repository "deb http://zeroc.com/download/ice/3.7/ubuntu20.04 stable main" && \
    wget -qO - https://svn.mpia.de/repo/linux/ubuntu/archive.key | apt-key add - && \
    echo "deb https://svn.mpia.de/repo/linux/ubuntu focal main" > /etc/apt/sources.list.d/mpia.list

RUN apt update -y
RUN apt install -y sudo subversion git lsof

RUN apt update -y
RUN apt install -y python3-setuptools python3-pip python3-toml git
RUN pip3 install numpy astropy sdss-clu
RUN apt install -y packagekit-gtk3-module python3-opencv tan-basda-mocca
RUN cd /root && \
    git clone https://github.com/sdss/lvmtan.git && \
    (cd lvmtan && python3 setup.py install || echo "fix me") && \
    cp lvmtan/container/run-basdard.sh . && \
    rm -rf lvmtan

#WORKDIR /root/lvm

CMD ["/root/run-basdard.sh"]
