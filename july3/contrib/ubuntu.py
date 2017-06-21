from july3.rule import Rule
from july3.util import run


class DebianPackage(Rule):

    def __init__(self, packages, dependencies=None):
        self.packages = packages
        super().__init__(str(self), dependencies)

    def is_made(self):
        return run("dpkg-query -Wf'${db:Status-abbrev}' %s" % ' '.join(self.packages), capture=True).returncode == 0

    def updated(self):
        return 0

    def __str__(self):
        return 'apt-get install %s' % ' '.join(self.packages)

    @staticmethod
    def command(rule):
        run('sudo apt-get install --quiet -y %s' % ' '.join(rule.packages))


class Command(Rule):

    def is_made(self):
        return run('type {0}'.format(self.target), capture=True).returncode == 0


    def updated(self):
        return 0