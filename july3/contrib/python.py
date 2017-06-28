import os

from july3 import env
from july3.rule import Rule
from july3.util import sh, sudo_cmd


class PythonPackage(Rule):

    def __init__(self, *packages, dependencies=None, pip='pip3', virtualenv=None, sudo=False):
        self.packages = packages
        self.pip = pip
        self.virtualenv = virtualenv
        self.sudo = sudo

        super().__init__(str(self), dependencies)

    def is_made(self):
        return set(self.packages).issubset(
            {package.split(' ')[0] for package in sh('{0} list --format=legacy'.format(self.pip), capture=True).stdout.splitlines()}
        )

    def updated(self):
        return 0

    def __str__(self):
        return 'pip install %s' % ' '.join(self.packages)

    @staticmethod
    def command(rule):
        packages = ' '.join(rule.packages)
        pip(f'install {packages}', pip=rule.pip, virtualenv=rule.virtualenv, sudo=rule.sudo)


def pip(command, pip='pip3', virtualenv=None, sudo=False):
    pip_cmd = pip

    if virtualenv:
        pip_cmd = virtualenv + '/bin/' + pip_cmd

    pip_cmd = sudo_cmd(sudo) + pip_cmd
    sh(f'{pip_cmd} {command}')


class PythonRequirements(Rule):
    def __init__(self, requirements, dependencies=None, pip='pip3', virtualenv=None, sudo=False):

        self.requirements = requirements
        self.pip = pip
        self.virtualenv = virtualenv
        self.sudo = sudo

        super().__init__(str(self), dependencies)

    def is_made(self):
        return False

    def updated(self):
        return 0

    def __str__(self):
        return f'pip install -r {self.requirements}'

    @staticmethod
    def command(rule):
        pip(f'install -r {rule.requirements}')


class Virtualenv(Rule):
    def __init__(self, target, python='python', dependencies=None):
        self.python = python

        super().__init__(target, dependencies)

    def is_made(self):
        return os.path.exists(self.target + '/bin/python')

    def updated(self):
        if self.is_made():
            return os.path.getmtime(self.target + '/bin/python')
        return 0

    @staticmethod
    def command(rule):
        sh(f'{rule.python} -m venv {env.virtualenv}')