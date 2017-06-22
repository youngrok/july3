import os

from july3 import env
from july3.rule import Rule
from july3.util import run


class PythonPackage(Rule):

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
    def command(rule):
        packages = ' '.join(rule.packages)
        run(f'{rule.pip} install {packages}')


class Virtualenv(Rule):
    def __init__(self, target, dependencies=None):
        if not dependencies:
            dependencies = []
        dependencies.append(PythonPackage('virtualenv', sudo=True))
        super().__init__(target, dependencies)

    def is_made(self):
        return os.path.exists(self.target + '/bin/python')

    def updated(self):
        if self.is_made():
            return os.path.getmtime(self.target + '/bin/python')
        return 0

    @staticmethod
    def command(rule):
        run('virtualenv {virtualenv}'.format_map(env))