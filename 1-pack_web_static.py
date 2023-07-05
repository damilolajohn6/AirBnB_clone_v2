from fabric.api import local
from datetime import datetime

def do_pack():
    """Create a tar gzipped archive of the directory web_static."""
    dt = datetime.utcnow()
    file = "versions/web_static_{}{}{}{}{}{}.tgz".format(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)
    if local("mkdir -p versions").failed is True:
        return None
    if local("tar -cvzf {} web_static".format(file)).failed is True:
        return None
    return file

def do_deploy(archive_path):
    """Deploy the web_static content to the web servers"""
    if not os.path.isfile(archive_path):
        return False

    try:
        file_name = archive_path.split('/')[-1]
        file_no_ext = file_name.split('.')[0]
        releases_path = '/data/web_static/releases/'
        tmp_path = '/tmp/'

        put(archive_path, tmp_path)
        run('mkdir -p {}{}/'.format(releases_path, file_no_ext))
        run('tar -xzf {}{} -C {}{}/'.format(tmp_path, file_name, releases_path, file_no_ext))
        run('rm {}'.format(tmp_path + file_name))
        run('mv {0}{1}/web_static/* {0}{1}/'.format(releases_path, file_no_ext))
        run('rm -rf {}{}/web_static'.format(releases_path, file_no_ext))
        run('rm -rf /data/web_static/current')
        run('ln -s {}{}/ /data/web_static/current'.format(releases_path, file_no_ext))
        return True
    except:
        return False
