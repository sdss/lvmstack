# lvmtan

![Versions](https://img.shields.io/badge/python->3.7-blue)
[![Documentation Status](https://readthedocs.org/projects/sdss-lvmtan/badge/?version=latest)](https://sdss-lvmtan.readthedocs.io/en/latest/?badge=latest)
[![Travis (.org)](https://img.shields.io/travis/sdss/lvmtan)](https://travis-ci.org/sdss/lvmtan)
[![codecov](https://codecov.io/gh/sdss/lvmtan/branch/main/graph/badge.svg)](https://codecov.io/gh/sdss/lvmtan)

Lvm Tan Clu Wrapper


## Features


- CLU based wrapper for TwiceAsNice.
- Uses a container for deployment and testing. 


## Installation

This package is used for building the TwiceAsNice container and running tests.



    git clone https://github.com/wasndas/lvmtan.git
    cd lvmtan
    

### Centos


    # as user 
    python3.8  -m pip  install --user --upgrade pip
    pip3.8 install poetry
    export PATH=~/.local/bin/:$PATH
   
## Quick start
-----------

    poetry update
    poetry run pytest -p no:logging -s -v 
    poetry run pytest -p no:logging -s -v --runslow
