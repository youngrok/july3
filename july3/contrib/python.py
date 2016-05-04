import os

from july3 import env
from july3.target import Target
from july3.util import run


class PythonPackage(Target):

    def __init__(self, *packages, pip='pip3', virtualenv=None, sudo=False, dependencies=None):
        self.packages = packages
        self.virtualenv = virtualenv
        self.pip = pip
        if virtualenv:
            self.pip = self.virtualenv + '/bin/' + self.pip
        if sudo:
            self.pip = 'sudo ' + self.pip

        super().__init__(str(self), dependencies)

    def is_made(self):
        return set(self.packages).issubset(
            {package.split(' ')[0] for package in run('{0} list'.format(self.pip), capture=True).stdout.splitlines()}
        )

    def updated(self):
        return 0

    def __str__(self):
        return 'pip install %s' % ' '.join(self.packages)

    @staticmethod
    def command(target):
        run('{0} install {packages}'.format(target.pip, packages=' '.join(target.packages)))


class PyEnv(Target):
    def __init__(self, name, dependencies=None):
        if not dependencies:
            dependencies = []
        dependencies.append(PythonPackage('virtualenv', sudo=True))
        super().__init__(name, dependencies)

    def is_made(self):
        return os.path.exists(self.name + '/bin/python')

    def updated(self):
        if self.is_made():
            return os.path.getmtime(self.name + '/bin/python')
        return 0

    @staticmethod
    def command(target):
        run('virtualenv {virtualenv}'.format_map(env))