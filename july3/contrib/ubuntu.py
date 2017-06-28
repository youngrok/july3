from july3.rule import Rule
from july3.util import sh


class DebianPackage(Rule):

    def __init__(self, packages, dependencies=None):
        self.packages = packages
        super().__init__(str(self), dependencies)

    def is_made(self):
        result = sh("dpkg-query -Wf'${db:Status-abbrev}' %s" % ' '.join(self.packages), capture=True)
        return result.returncode == 0 and all([status == 'ii' for status in result.stdout.split(' ') if status])

    def updated(self):
        return 0

    def __str__(self):
        return 'apt-get install %s' % ' '.join(self.packages)

    @staticmethod
    def command(rule):
        sh('sudo apt-get install --quiet -y %s' % ' '.join(rule.packages))


class Command(Rule):

    def is_made(self):
        return sh('type {0}'.format(self.target), capture=True).returncode == 0


    def updated(self):
        return 0