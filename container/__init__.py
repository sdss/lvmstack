# -*- coding: utf-8 -*-
#
# @Author: Florian Briegel (briegel@mpia.de
# @Date: 2021-06-15
# @Filename: __init__.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

import os
import shlex
import subprocess
import sys
import time
from pathlib import PosixPath

import click
import pexpect


# from podman import PodmanClient
# uri = "unix:///run/user/1000/podman/podman.sock"
# podman container exists ubuntu_lvmt_tan # 0=True, 1=False


container_bin = "podman"
lvm_root = os.environ["PWD"]
lvm_image_source_local = "localhost"
lvm_image_source_remote = "ghcr.io/sdss"
lvm_image_name = "lvmtan"

default_basdard_test = "test.first.focus_stage"


def config(name, pstfx="-sim.conf"):
    return f"{'/'.join(str.split(name,'.')[:-1])}/{name}{pstfx}"


def isRunning(name: str = default_basdard_test):
    command = subprocess.run(shlex.split(f"{container_bin} container exists {name}"))
    return not command.returncode  # True if running


def getXauthority():
    for xa in [f"/run/user/{os.getuid()}/gdm/Xauthority", "~/.Xauthority"]:
        xa = PosixPath(xa).expanduser()
        if xa.exists():
            return xa
    return None


@click.command()
@click.option("--lvm_root", default=lvm_root, type=str)
@click.option("--use-cache/--no-cache", default=True)
def build(lvm_root: str, use_cache: bool):
    tan_dockerfile = f"{lvm_root}/container"
    lvm_image_fullbuild = "" if use_cache else " --no-cache"
    print(
        f"{container_bin} build --tag {lvm_image_name}{lvm_image_fullbuild} --rm {tan_dockerfile}"
    )
    build = f"{container_bin} build --tag {lvm_image_name}{lvm_image_fullbuild} --rm {tan_dockerfile}"
    command = subprocess.run(shlex.split(build))


@click.command()
@click.option("--lvm_root", default=lvm_root, type=str)
@click.option("--lvm_rmq", default=None, type=str)
@click.option("--with-ui/--without-ui", default=True)
@click.option("--with-hw/--without-hw", default=False)
@click.option("--debug/--no-debug", "-d", default=False)
@click.option("--kill/--no-kill", default=False)
@click.option("--name", "-n", default=default_basdard_test, type=str)
def start(name: str, with_ui: bool, with_hw: bool, lvm_root: str, lvm_rmq:str, debug:bool, kill:bool):
    if not subprocess.run(shlex.split(f"podman image exists {lvm_image_source_local}/{lvm_image_name}")).returncode:
       lvm_image = f"{lvm_image_source_local}/{lvm_image_name}"
    else:
       if subprocess.run(shlex.split(f"podman image exists {lvm_image_source_remote}/{lvm_image_name}")).returncode:
           subprocess.run(shlex.split(f"podman pull {lvm_image_source_remote}/{lvm_image_name}:latest"))
       lvm_image = f"{lvm_image_source_remote}/{lvm_image_name}"
    
    if kill:
        subprocess.run(shlex.split(f"{container_bin} kill {name}"))

    run_base = f"--rm -t --name {name} --network=host"
    if os.path.exists("/usr/bin/crun"):
        run_base += f" --runtime /usr/bin/crun"
    system_xauthority = getXauthority()
    if with_ui and os.environ.get("DISPLAY") and system_xauthority:
        run_base += f" -e DISPLAY -v {system_xauthority}:/root/.Xauthority:Z --ipc=host"
        if os.path.exists("/dev/dri"):
            run_base += " --device /dev/dri"
        name_ui = config(name, pstfx=".ui")
        if os.path.exists(f"{lvm_root}/config/{name_ui}"):
            run_base += f" -e BASDARD_UI={name_ui}"

    print(debug)
    if debug:
        run_base +=  f" -e LVM_DEBUG=true"

    if lvm_rmq:
        run_base +=  f" -e LVM_RMQ={lvm_rmq}"

    run_with_hw = "-svr.conf" if with_hw else "-sim.conf"
    run_tan = f"-v {lvm_root}:/root/lvm:Z -e BASDARD_CONFIG={config(name, pstfx = run_with_hw)}"
    run = f"{container_bin} run {run_base} {run_tan} {lvm_image}"
    print(run)
    child = pexpect.spawn(run)
    child.expect("Connected to")
    assert isRunning(name) == True


@click.command()
@click.option("--name", "-n", default=default_basdard_test, type=str)
def stop(name: str):
    command = subprocess.run(shlex.split(f"{container_bin} kill {name}"))
