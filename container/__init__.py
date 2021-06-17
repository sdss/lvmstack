import subprocess
import sys
# -*- coding: utf-8 -*-
#
# @Author: Florian Briegel (briegel@mpia.de
# @Date: 2021-06-15
# @Filename: __init__.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

import os
import time
import pexpect
import shlex
import click
from pathlib import PosixPath

#from podman import PodmanClient
#uri = "unix:///run/user/1000/podman/podman.sock"
#podman container exists ubuntu_lvmt_tan # 0=True, 1=False


container_bin = 'podman'
lvmt_root = os.environ["PWD"]
lvmt_image_name = 'ubuntu_lvmt_tan'

default_basdard_test = 'test.first.focus_stage'


def config(name, pstfx="-sim.conf"):
    return f"{'/'.join(str.split(name,'.')[:-1])}/{name}{pstfx}"

def isRunning(name: str = default_basdard_test):
    command = subprocess.run(shlex.split(f"{container_bin} container exists {name}"))
    return not command.returncode # True if running
  
@click.command()   
@click.option("--lvmt_root", default=lvmt_root, type=str)
@click.option("--use-cache/--no-cache", default=True)
def build(lvmt_root:str, use_cache: bool):
    tan_dockerfile = f"{lvmt_root}/container"
    lvmt_image_fullbuild = "" if use_cache else " --no-cache"
    print(f"{container_bin} build --tag {lvmt_image_name}{lvmt_image_fullbuild} --rm {tan_dockerfile}")
    build = f"{container_bin} build --tag {lvmt_image_name}{lvmt_image_fullbuild} --rm {tan_dockerfile}"
    command = subprocess.run(shlex.split(build))


@click.command()   
@click.option("--lvmt_root", default=lvmt_root, type=str)
@click.option("--with_ui/--without_ui", default=True)
@click.option("--name", "-n", default=default_basdard_test, type=str)
def start(name: str, with_ui: bool, lvmt_root:str):
    lvmt_image = f"localhost/{lvmt_image_name}"

    run_base = f"--rm -t --name {name} --network=host"
    if with_ui and os.environ.get("DISPLAY"):
        system_xauthority=PosixPath('~/.Xauthority').expanduser()
        run_base +=  f" -e DISPLAY -v {system_xauthority}:/root/.Xauthority:Z --ipc=host"
        if os.path.exists('/dev/dri'):
            run_base +=  ' --device /dev/dri'
        name_ui = config(name, pstfx=".ui")
        if os.path.exists(f"{lvmt_root}/config/{name_ui}"):
            run_base +=  f" -e BASDARD_UI={name_ui}"
    run_tan = f"-v {lvmt_root}:/root/lvmt:Z -e BASDARD_CONFIG={config(name)}"
    run = f"{container_bin} run {run_base} {run_tan} {lvmt_image}"
    child = pexpect.spawn(run)
    child.expect('Connected to')
    assert isRunning(name) == True
    

@click.command()   
@click.option("--name", "-n", default=default_basdard_test, type=str)
def stop(name: str):
    command = subprocess.run(shlex.split(f"{container_bin} kill {name}"))


