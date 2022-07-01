FROM ubuntu:22.04

## Get some karma ##
MAINTAINER Florian Briegel, briegel@mpia.de

# podman  build --tag lvm_actor --rm .

# podman run -ti --rm --name lvm_actor -v .:/root/lvm:Z -P localhost/lvm_actor

RUN apt update -y

RUN apt install -y pkg-config libgirepository1.0-dev \
                   libcairo2-dev gobject-introspection python3-gi \
                   gir1.2-aravis-0.8 aravis-tools aravis-tools-cli
 
RUN apt install -y python3-pip

RUN pip3 install sdss-lvmscraper \
                 sdss-lvmnps \
                 sdss-lvmcam \
                 sdss-lvmagp \
                 sdss-lvmieb \
                 sdss-lvmscp 
                 #sdss-lvmecp not available for 3.10
                 

WORKDIR /root

COPY run-actor.sh /root

CMD ["/root/run-actor.sh"]



