#!/usr/bin/python3
"""This module contains do_deploy function for distributing
an archive to web servers
"""
from fabric.api import run, env, put
from os import path


env.hosts = ['100.25.45.230', '54.175.100.32']


def do_deploy(archive_path):
    """distributes an archive to your web servers.

    args:
       archive_path: pathname to the archive to distribute.

    Functionality:
      - Uploads the archive to the /tmp/ directory of the web server
      - Uncompresses the archive to the folder /data/web_static/releases/
            <archive filename without extension> on the web server
      - Deletes the archive from the web server
      - Deletes the symbolic link /data/web_static/current from the web server
      - Creates a new the symbolic link /data/web_static/current on the
            web server, linked to the new version of your code
            (/data/web_static/releases/<archive filename without extension>)

    Returns:
       True if all operations have been done correctly, otherwise returns False
    """
    if path.isfile(archive_path) is False:
        return False
    filename = archive_path.split("/")[-1]
    Uncompfile = filename.split(".")[0]

    if put(archive_path, "/tmp/{}".format(filename)).failed is True:
        return False
    if run("rm -rf /data/web_static/releases/{}/".
           format(Uncompfile)).failed is True:
        return False
    if run("mkdir -p /data/web_static/releases/{}/".
           format(Uncompfile)).failed is True:
        return False
    if run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".
           format(filename, Uncompfile)).failed is True:
        return False
    if run("rm /tmp/{}".format(filename)).failed is True:
        return False
    if run("mv /data/web_static/releases/{}/web_static/* "
           "/data/web_static/releases/{}/".format(Uncompfile,
                                                  Uncompfile)).failed is True:
        return False
    if run("rm -rf /data/web_static/releases/{}/web_static".
           format(Uncompfile)).failed is True:
        return False
    if run("rm -rf /data/web_static/current").failed is True:
        return False
    if run("ln -s /data/web_static/releases/{}/ /data/web_static/current".
           format(Uncompfile)).failed is True:
        return False
    return True
