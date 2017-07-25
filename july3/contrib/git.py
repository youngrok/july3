import os.path

import time
from july3 import env
from july3.rule import Rule
from july3.util import sh


class GitPull(Rule):

    def __init__(self, url, path, dependencies=None):
        super().__init__('git clone %s %s' % (url, path), dependencies=dependencies)
        self.url = url
        self.path = path

        self.executed = False

    def is_made(self):
        return self.executed > 0

    def updated(self):
        return self.executed

    @staticmethod
    def command(rule):
        if os.path.exists(rule.path):
            sh("cd %s; ssh-agent bash -c 'ssh-add %s; git pull'" % (rule.path, env.deploy_key_file))
        else:
            sh("ssh-agent bash -c 'ssh-add %s; git clone %s %s'" % (env.deploy_key_file, rule.url, rule.path))

        rule.executed = time.time()