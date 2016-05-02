from july3.target import Target
from july3.util import run


class DebianPackage(Target):

    def __init__(self, packages, dependencies=None):
        self.packages = packages
        super().__init__(str(self), dependencies)

    def is_made(self):
        run("dpkg-query -Wf'${db:Status-abbrev}' %s" % ' '.join(self.packages))

    def updated(self):
        return 0

    def __str__(self):
        return 'apt-get install %s' % ' '.join(self.packages)

    @staticmethod
    def command(target):
        run('sudo apt-get install -y %s' % ' '.join(target.packages))
