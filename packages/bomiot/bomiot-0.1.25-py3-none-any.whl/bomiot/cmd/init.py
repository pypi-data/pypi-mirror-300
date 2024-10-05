from os.path import join, exists
from os import makedirs, getcwd, environ
import subprocess

def init(folder):
    """
    init workspace
    :param folder:
    :return:
    """
    cmd = "bomiot makemigrations"
    subprocess.run(cmd, shell=True)

    log_path = join(getcwd(), 'logs')
    exists(log_path) or makedirs(log_path)
    environ.setdefault('RUN_MAIN', 'true')

    print(environ.get("RUN_MAIN"))
    print('Initialized workspace %s' % folder)
