#!/usr/bin/python3
# Fabfile to delete out-of-date archives.
import os
from fabric.api import *

env.hosts = ["54.160.85.72", "35.175.132.106"]


def do_clean(number=0):
    """Delete out-of-date archives.

    Args:
        number (int): The number of archives to keep.
            If number is 0 or 1, keeps only the most recent archive.
            If number is 2, keeps the most and second-most recent archives, etc.
    """
    number = int(number)
    number = max(number, 1)

    with lcd("versions"):
        archives = sorted(os.listdir("."))
        archives_to_delete = archives[:-number]
        [local("rm {}".format(archive)) for archive in archives_to_delete]

    with cd("/data/web_static/releases"):
        archives = run("ls -t").split()
        archives = [archive for archive in archives if "web_static_" in archive]
        archives_to_delete = archives[:-number]
        [run("rm -rf {}".format(archive)) for archive in archives_to_delete]
