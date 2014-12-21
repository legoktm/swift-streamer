#!/usr/bin/env python2
from fabric.api import *  # noqa
import fabric.contrib.project as project

import config

# Local path configuration (can be absolute or relative to fabfile)
env.deploy_path = config.OUTPUT
DEPLOY_PATH = env.deploy_path

env.hosts = [config.REMOTE_SERVER]
env.use_ssh_config = True
dest_path = config.REMOTE_LOCATION


def clean():
    local('rm -rfv output')


def build():
    local('~/python3/bin/python build.py')


def publish():
    build()
    sync()


def sync():
    project.rsync_project(
        remote_dir=dest_path,
        exclude=".idea/",
        local_dir=DEPLOY_PATH.rstrip('/') + '/',
        delete=True,
        extra_opts='-c',
    )
