#!/usr/bin/python3
"""This module contains a fabric based function to generate
a .tgz archive from the web_static directory.
"""
from fabric.api import local
from datetime import datetime
from os import path


def do_pack():
    """generates a .tgz archive from the contents of the web_static

    Functionality:
      - Creates a directory versions
      - Collects a file in we' '

    Returns:
        return the archive path if the archive has been correctly
        generated. Otherwise, it should return None
    """
    date = str(datetime.utcnow().date()).replace('-', '')
    time = str(datetime.utcnow().time()).replace(':', '').split('.')[0]
    if time[0] == '0':
        time = time[1:]
    if not path.exists('versions'):
        local('mkdir -p versions')
    else:
        print("already exists")
    arch = "versions/web_static{}{}.tgz".format(date, time)
    result = local('tar -cvzf {} web_static'.format(arch)).failed

    if path.exists(arch) and result is False:
        return arch
    else:
        return None
