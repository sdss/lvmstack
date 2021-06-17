# lvmtan

![Versions](https://img.shields.io/badge/python->3.7-blue)
[![Documentation Status](https://readthedocs.org/projects/sdss-lvmtan/badge/?version=latest)](https://sdss-lvmtan.readthedocs.io/en/latest/?badge=latest)
[![Travis (.org)](https://img.shields.io/travis/sdss/lvmtan)](https://travis-ci.org/sdss/lvmtan)
[![codecov](https://codecov.io/gh/sdss/lvmtan/branch/main/graph/badge.svg)](https://codecov.io/gh/sdss/lvmtan)

Lvm Tan Clu Wrapper

This package is used for building the TwiceAsNice container and running tests.

## Features

- CLU based wrapper for TwiceAsNice.
- Uses a container for deployment and testing. 

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
    zypper ar https://download.opensuse.org/repositories/devel:/languages:/python:/Factory/openSUSE_Leap_15.2/
    zypper install python39
    # as user 
    python3.9  -m pip  install --user --upgrade pip
    pip3.9 install poetry
    export PATH=~/.local/bin/:$PATH

## Quick start

### Download
    git clone https://github.com/wasndas/lvmtan.git
    cd lvmtan      

### Build
    # build sdist & wheel
    poetry build
    
    # update local py env
    poetry update
    
    # build tan container
    poetry run container_build
    # build tan container from scratch
    poetry run container_build --no-cache
        
### Run container (optional)

    # default config test.first.focus_stage-sim.conf
    poetry run container_start
    poetry run container_stop
    
    # all stages config lvm.all-sim.conf
    poetry run container_start --name lvm.all
    poetry run container_stop --name lvm.all


### Run tests 

    # run tests
    poetry run pytest
    # ... with slow tests with enabled log to stdout
    poetry run pytest -p no:logging -s -v --runslow
    # ... only test 02
    poetry run pytest -k test_02_lvm_all.py
    # ... without UI
    DISPLAY= poetry run pytest -p no:logging -s -v -k test_02_lvm_all.py
    
    
### Publish
    # publish to pypi
    poetry publish --username=USER --password=PASS
