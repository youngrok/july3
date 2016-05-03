from july3 import env
from july3.target import Target
from july3.util import run


class PythonPackage(Target):

    def __init__(self, *packages, virtualenv=None, dependencies=None):
        self.packages = packages
        self.virtualenv = virtualenv
        self.pip = 'pip'
        if virtualenv:
            self.pip = self.virtualenv + '/' + self.pip

        super().__init__(str(self), dependencies)

    def is_made(self):
        return set(self.packages).issubset(
            {package.split(' ')[0] for package in run('{0} list'.format(self.pip)).stdout.splitlines()}
        )

    def updated(self):
        return 0

    def __str__(self):
        return 'pip install %s' % ' '.join(self.packages)

    @staticmethod
    def command(target):
        run('{0} install {packages}'.format(target.pip, packages=' '.join(target.packages)))