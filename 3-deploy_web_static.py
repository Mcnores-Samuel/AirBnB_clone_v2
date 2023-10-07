#!/usr/bin/python3
"""This module contains a fabric based function that
creates and distributes an archive to web servers,
using the function deploy:
"""
from fabric.api import local, runs_once
from datetime import datetime
from os import path
from fabric.api import run, env, put


env.hosts = ['100.25.45.230', '54.175.100.32']


@runs_once
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
    arch = "versions/web_static_{}{}.tgz".format(date, time)
    result = local('tar -cvzf {} web_static'.format(arch)).failed

    if path.exists(arch) and result is False:
        return arch
    else:
        return None


def do_deploy(archive_path):
    """distributes an archive to web servers.

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
    if not path.exists(archive_path):
        return False

    filename = path.basename(archive_path)
    releases = "/data/web_static/releases"
    uncompfile = path.splitext(filename)[0]

    try:
        put(archive_path, '/tmp/')

        run('mkdir -p {}/{}'.format(releases, uncompfile))
        run('tar -xzf /tmp/{} -C {}/{}/'.format(filename, releases,
                                                uncompfile))

        run('rm /tmp/{}'.format(filename))

        run('rsync -a {}/{}/web_static/ {}/{}'.format(
            releases, uncompfile, releases, uncompfile))
        run('rm -rf {}/{}/web_static/'.format(releases, uncompfile))

        run('rm -rf /data/web_static/current')
        run('ln -s {}/{} /data/web_static/current'.format(releases,
                                                          uncompfile))

        return True
    except Exception:
        return False


def deploy():
    """creates and distributes an archive to web servers"""
    pathname = do_pack()
    if not pathname:
        return False
    return do_deploy(pathname)
