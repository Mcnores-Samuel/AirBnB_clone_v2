#!/usr/bin/python3
"""This module contains do_clean function with removes/deletes
old archives from both local and removes servers.
"""
from fabric.api import local, env, run, runs_once, cd
import os


env.hosts = ['100.25.45.230', '54.175.100.32']


@runs_once
def do_clean_local(number):
    """Deletes the all archives except the latest specified to be keep
    in the number.
    all deletion is done locally.
    """
    versions = "versions"

    sorted_list = []
    all_files = []

    for root, dirs, files in os.walk(versions):
        for filename in files:
            all_files.append(filename)
            file_path = os.path.join(root, filename)
            file_path = file_path.split('/')[1].split('_')[-1].split('.')[0]
            sorted_list.append(int(file_path))
    sorted_list = sorted(sorted_list)

    for date in sorted_list[:number]:
        for file in all_files:
            if str(date) in file:
                if os.path.exists("{}/{}".format(versions, file)):
                    local('rm {}/{}'.format(versions, file))


def do_clean_remote(number):
    """Deletes all older versions of the archives on a remote servers"""
    with cd("/data/web_static/releases"):
        archives = run("ls -tr").split()
        archives = [a for a in archives if "web_static_" in a]
        [archives.pop() for i in range(number)]
        [run("rm -rf ./{}".format(a)) for a in archives]


def do_clean(number=0):
    """Deletes older archives on both remote and local servers"""
    if number == 0 or number == 1:
        number = -1
    else:
        number = int(number) * -1

    do_clean_local(number)
    n = abs(number)
    do_clean_remote(n)
