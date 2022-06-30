FROM ubuntu:22.04

## Get some karma ##
MAINTAINER Florian Briegel, briegel@mpia.de

# podman  build --tag lvm_actor --rm .

# podman run -ti --rm --name lvmt_cam -v .:/root/lvmt:Z -P localhost/lvm_actor

# RUN apt update -y && \
#     apt install -y wget && \
#     echo "8\n7\n" | apt install -y software-properties-common && \
#     echo "30\n1\n" | apt install -y keyboard-configuration


RUN apt update -y

RUN apt install -y sudo git lsof pkg-config libgirepository1.0-dev libcairo2-dev gobject-introspection python3-gi
RUN apt install -y gir1.2-aravis-0.8 aravis-tools aravis-tools-cli
 
RUN apt install -y python3-pip

RUN pip3 install sdss-clu \
                 sdss-cluplus \
                 sdss-lvmtipo \
                 sdss-lvmnps \
                 sdss-lvmcam \
                 sdss-lvmagp \
                 sdss-lvmieb \
                 sdss-lvmscp 
                 #sdss-lvmecp not available for 3.10
                 

WORKDIR /root

COPY run-actor.sh /root

CMD ["/root/run-actor.sh"]



