from july3 import env
from july3.target import Target
from july3.util import run


class PythonPackage(Target):

    def __init__(self, *packages, dependencies=None):
        self.packages = packages
        super().__init__(str(self), dependencies)

    def is_made(self):
        return set(self.packages).issubset(
            {package.split(' ')[0] for package in run('pip list').stdout.splitlines()}
        )

    def updated(self):
        return 0

    def __str__(self):
        return 'pip install %s' % ' '.join(self.packages)

    @staticmethod
    def command(target):
        run('pip install %s' % ' '.join(target.packages))