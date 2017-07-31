import time
from july3.rule import Rule, OnceRule
from july3.util import sh


class DebianPackage(OnceRule):

    def __init__(self, packages, dependencies=None):
        self.packages = packages
        super().__init__(str(self), dependencies)

    def is_made(self):
        result = sh("   dpkg-query -Wf'${db:Status-abbrev}' %s" % ' '.join(self.packages), capture=True)
        return result.returncode == 0 and all([status == 'ii' for status in result.stdout.split(' ') if status])

    def __str__(self):
        return 'apt-get install %s' % ' '.join(self.packages)

    @staticmethod
    def command(rule):
        sh('DEBIAN_FRONTEND=noninteractive sudo apt-get install --quiet -y %s' % ' '.join(rule.packages))
