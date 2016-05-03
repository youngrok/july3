import os.path

from july3 import env
from july3.target import Target
from july3.util import run


class GitUpdated(Target):

    def __init__(self, url, path, dependencies=None):
        super().__init__('git clone %s %s' % (url, path), dependencies=dependencies)
        self.url = url
        self.path = path

    def is_made(self):
        return False

    @staticmethod
    def command(target):
        if os.path.exists(target.path):
            run("cd %s; ssh-agent bash -c 'ssh-add %s; git pull'" % (target.path, env.deploy_key_file))
        else:
            run("ssh-agent bash -c 'ssh-add %s; git clone %s %s'" % (env.deploy_key_file, target.url, target.path))