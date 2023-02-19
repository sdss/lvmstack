# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
ARG OWNER=jupyter
ARG BASE_CONTAINER=$OWNER/scipy-notebook
FROM $BASE_CONTAINER

#LABEL maintainer="Jupyter Project <jupyter@googlegroups.com>"
## Get some karma ##
MAINTAINER Florian Briegel, briegel@mpia.de

RUN pip3 install sdss-lvmtipo sdss-cluplus sdss-lvmagp
RUN pip3 install astrometry reproject astroquery
RUN pip3 install ipydatagrid
RUN pip3 install jupyter-app-launcher

RUN pip3 install pywwt
RUN pip install wwt-kernel-data-relay && \
    jupyter labextension install --no-build @jupyter-widgets/jupyterlab-manager && \
    jupyter labextension install --no-build @wwtelescope/jupyterlab && \
    jupyter lab build

USER root

RUN mkdir /usr/local/bin/start-notebook.d
RUN printf '\n\
LVM_ROOT=$HOME\n\
if [ ${LVM_DEBUG} ]; then\n\
  export PYTHONPATH=${LVM_ROOT}/examples:$(ls -1 -d ${LVM_ROOT}/lvm/*/python ${LVM_ROOT}/lvm/basecam ${LVM_ROOT}/lvm/araviscam 2>/dev/null | tr "\n" ":")\n\
fi\n\

' > /usr/local/bin/start-notebook.d/debug_env.sh
RUN chmod 755 /usr/local/bin/start-notebook.d/debug_env.sh


USER ${NB_UID}

RUN printf '\n\
. /usr/local/bin/start-notebook.d/debug_env.sh\n\
' >> /home/${NB_USER}/.bashrc

