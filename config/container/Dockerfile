FROM ubuntu:20.04

## Get some karma ##
MAINTAINER Florian Briegel, briegel@mpia.de

# podman  build --tag ubuntu_lvmt_core --rm lvmt_core

# podman run -ti --rm --name lvmt_core -v .:/root/lvmt:Z -P localhost/ubuntu_lvmt_core

RUN apt update -y && \
    apt install -y wget && \
    echo "8\n7\n" | apt install -y software-properties-common && \
    echo "30\n1\n" | apt install -y keyboard-configuration && \
    wget -qO - https://svn.mpia.de/repo/linux/ubuntu/archive.key | apt-key add - && \
    echo "deb https://svn.mpia.de/repo/linux/ubuntu focal main" > /etc/apt/sources.list.d/mpia.list

RUN apt update -y
RUN apt install -y sudo git lsof
RUN apt install -y gir1.2-aravis-0.8 aravis-tools aravis-tools-cli
RUN apt install -y pip python3.9
RUN python3.9 -m pip install --upgrade pip

RUN pip3.9 install sdss-skymakercam

RUN apt update -y
#RUN apt install -y python3-setuptools python3-pip python3-toml git
#RUN apt install -y packagekit-gtk3-module 


WORKDIR /root/lvmt

#COPY run-basdard.sh /root

CMD ["/root/run-now.sh"]
