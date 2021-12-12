# lvmtan

![Versions](https://img.shields.io/badge/python->3.7-blue)
[![Documentation Status](https://readthedocs.org/projects/sdss-lvmtan/badge/?version=latest)](https://sdss-lvmtan.readthedocs.io/en/latest/?badge=latest)
[![Travis (.org)](https://img.shields.io/travis/sdss/lvmtan)](https://travis-ci.org/sdss/lvmtan)
[![codecov](https://codecov.io/gh/sdss/lvmtan/branch/main/graph/badge.svg)](https://codecov.io/gh/sdss/lvmtan)

Lvm Tan Clu Wrapper

## Features

- CLU based wrapper for [TwiceAsNice](https://svn.mpia.de/trac/gulli/TwiceAsNice/)
- Uses a container for deployment and testing. 
- Uses podman¹ for building the container.

¹ Setting an alias to use docker might work.

    alias podman="sudo docker"
    
## Note

As of version 0.0.9 the container is renamed from ubuntu_lvmt_tan to lvmtan

## Quickstart
Beginning with version  0.0.9 the container doesnt have to be build, a container is download automatically from github.

    git clone https://github.com/sdss/lvmtan.git
    cd lvmtan      
    poetry run container_start --kill --name lvm.all

## Prerequisites

Some linux distributions do not have python >= 3.7 as the standard python3 version.

### Centos 8.X

    # as root
    yum install python38
    # as user 
    python3.8  -m pip  install --user --upgrade pip
    pip3.8 install poetry
    export PATH=~/.local/bin/:$PATH

### OpenSuSe 15.2/15.3

    # as root
    zypper ar https://download.opensuse.org/repositories/devel:/languages:/python:/Factory/openSUSE_Leap_15.2/ devel_python
    zypper install python39-devel
    # as user 
    python3.9 -m ensurepip --default-pip # Alternatve: python3.9 -m venv ~/.local 
    pip3.9 install --upgrade pip
    pip3.9 install poetry
    export PATH=~/.local/bin/:$PATH

For running tests or containers a running RabbitMQ on localhost is expected with guest/guest

## Download
    git clone https://github.com/sdss/lvmtan.git
    cd lvmtan      


## Build
    # update local py env
    poetry update
    
    # build sdist & wheel
    poetry build
    
    # build tan container
    poetry run container_build
    # rebuild tan container from scratch
    poetry run container_build --no-cache
        
## Run container

    # default config test.first.focus_stage-sim.conf
    poetry run container_start
    poetry run container_stop
    
    # all stages config lvm.all-sim.conf
    poetry run container_start --name lvm.all
    poetry run container_stop --name lvm.all
  
    # all stages config lvm.all-sim.conf and kill running container
    poetry run container_start --kill --name lvm.all

    # log of the running container, -f output appended data as the file grows.
    podman logs -f lvm.all

    # config test.first.focus_stage-svr.conf with real hardware
    poetry run container_start --with-hw
    poetry run container_stop
    
    # derotator km with real hardware - check confige file config/test/derot/test.derot.km-dev.conf for correct MOD.TRAJ.CFG.CONNECTION.ADDRESS and MOD.TRAJ.CFG.CONNECTION.MODULE parameters
    poetry run container_start --name test.derot.km --with-hw
    
    # debug option, the local version is used instead of the latest github version when the container was built.
    poetry run container_start --debug
    
## Run tests 

    # run tests
    poetry run pytest
    # ... include slow tests with enabled log to stdout
    poetry run pytest -p no:logging -s -v --runslow
    # ... only test 02
    poetry run pytest -k test_02_lvm_all.py
    # ... without UI
    DISPLAY= poetry run pytest -p no:logging -s -v -k test_02_lvm_all.py
    
    
## Publish
    # publish to pypi
    poetry publish --username=USER --password=PASS
    # build rpm package
    poetry run python setup.py bdist_rpm
    # build deb package - needs python3-stdeb
    poetry run python setup.py --command-packages=stdeb.command bdist_deb
