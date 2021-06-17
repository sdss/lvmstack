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
#container_uri = "unix:///run/user/1000/podman/podman.sock"
#podman container exists ubuntu_lvmt_tan # 0=True, 1=False


podman_bin = 'podman'
lvmt_root = os.environ["PWD"]
lvmt_image_name = 'ubuntu_lvmt_tan'

default_basdard_test = 'test.first.focus_stage'


def container_config(name, pstfx="-sim.conf"):
    return f"{'/'.join(str.split(name,'.')[:-1])}/{name}{pstfx}"

def container_isRunning(name: str = default_basdard_test):
    command = subprocess.run(shlex.split(f"{use_container} container exists {name}"))
    return not command.returncode # True if running
  
@click.command()   
@click.option("--lvmt_root", default=lvmt_root, type=str)
@click.option("--use-cache/--no-cache", default=True)
@click.option("--use-container", default=podman_bin, type=str)
def container_build(lvmt_root:str, use_cache: bool, use_container: str):
    tan_dockerfile = f"{lvmt_root}/container"
    lvmt_image_fullbuild = "" if use_cache else " --no-cache"
    print(f"{use_container} build --tag {lvmt_image_name}{lvmt_image_fullbuild} --rm {tan_dockerfile}")
    build = f"{use_container} build --tag {lvmt_image_name}{lvmt_image_fullbuild} --rm {tan_dockerfile}"
    command = subprocess.run(shlex.split(build))


@click.command()   
@click.option("--lvmt_root", default=lvmt_root, type=str)
@click.option("--with-ui/--without-ui", default=True)
@click.option("--name", "-n", default=default_basdard_test, type=str)
@click.option("--use-container", default=podman_bin, type=str)
def container_run(name: str, with_ui: bool, lvmt_root: str, use_container: str):
    lvmt_image = f"localhost/{lvmt_image_name}"

    run_base = f"--rm -t --name {name} --network=host"
    if with_ui and os.environ.get("DISPLAY"):
        system_xauthority=PosixPath('~/.Xauthority').expanduser()
        run_base +=  f" -e DISPLAY -v {system_xauthority}:/root/.Xauthority:Z --ipc=host"
        if os.path.exists('/dev/dri'):
            run_base +=  ' --device /dev/dri'
        name_ui = container_config(name, pstfx=".ui")
        if os.path.exists(f"{lvmt_root}/config/{name_ui}"):
            run_base +=  f" -e BASDARD_UI={name_ui}"
    run_tan = f"-v {lvmt_root}:/root/lvmt:Z -e BASDARD_CONFIG={container_config(name)}"
    run = f"{use_container} run {run_base} {run_tan} {lvmt_image}"
    child = pexpect.spawn(run)
    child.expect('Connected to')
    assert container_isRunning(name) == True
    

@click.command()   
@click.option("--name", "-n", default=default_basdard_test, type=str)
@click.option("--use-container", default=podman_bin, type=str)
def container_kill(name: str, use_container: str):
    command = subprocess.run(shlex.split(f"{use_container} kill {name}"))


