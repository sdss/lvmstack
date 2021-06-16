import subprocess
import sys
import os
import pexpect
import shlex
from pathlib import PosixPath

from podman import PodmanClient

system_xauthority=PosixPath('~/.Xauthority').expanduser()

podman_lvmt_root = '/home/briegel/workspace/lvmt/'

podman_lvmt_image_name = 'ubuntu_lvmt_tan'
podman_lvmt_image = f"localhost/{podman_lvmt_image_name}"

podman_lvmt_tan_cmd = 'run-basdard.sh'
podman_lvmt_tan_conf = 'test/first/test.first.focus_stage-sim.conf'
podman_lvmt_tan_dockerfile = f"{podman_lvmt_root}/podman/lvmt_tan"
podman_lvmt_name = podman_lvmt_tan_conf.split("/")[-1][0:-5]

podman_uri = "unix:///run/user/1000/podman/podman.sock"
podman_bin = 'podman'


podman_build = f"{podman_bin} build --tag {podman_lvmt_image_name} --rm {podman_lvmt_tan_dockerfile}"


podman_run_base = f"--rm -ti --name {podman_lvmt_image_name} --network=host"
if os.environ.get("DISPLAY"):
     podman_run_base +=  f" -e DISPLAY -v {system_xauthority}:/root/.Xauthority:Z --ipc=host"
     if os.path.exists('/dev/dri'):
         podman_run_base +=  ' --device /dev/dri'

podman_run_tan = f"-v {podman_lvmt_root}:/root/lvmt:Z -e BASDARD_CONFIG={podman_lvmt_tan_conf}"
podman_run = f"{podman_bin} run {podman_run_base} {podman_run_tan} {podman_lvmt_image} {podman_lvmt_tan_cmd}"

podman_test_tan = f"{podman_bin} exec -t {podman_lvmt_image_name}"


client = PodmanClient(uri=podman_uri)
print(client.version())

#client.images.remove(podman_lvmt_image)
if not client.images.exists(podman_lvmt_image):
   # doesnt work :-(
   #client.images.build(path='/home/briegel/workspace/lvmt/podman', tag='lvmt', rm=True, quiet=False, forcerm=True, dockerfile='/home/briegel/workspace/lvmt/podman/Dockerfile')
   command = subprocess.run(shlex.split(podman_build))


# uncomplete
#client.containers.run(image=podman_lvmt_image,auto_remove=True,tty=True,command="/usr/bin/bash",network_mode="host",name=podman_lvmt_image_name,...)
#code is doc
#https://github.com/containers/podman-py/blob/b5337a5fa00d74010614567122a89fb44200ad02/podman/domain/containers_create.py
#https://github.com/containers/podman-py/blob/b5337a5fa00d74010614567122a89fb44200ad02/podman/domain/containers_create.py
#command = subprocess.run(shlex.split(podman_run))
child = pexpect.spawn(podman_run)
child.expect('Connected to')


command = subprocess.run(shlex.split(f"{podman_test_tan} /usr/bin/bash -l -c test.first.focus_stage_clu.py"))

command = subprocess.run(shlex.split(f"{podman_bin} kill {podman_lvmt_image_name}"))

#child = pexpect.spawn(podman_build)
#child.expect('Trying')


