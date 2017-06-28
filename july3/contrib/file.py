import os

from july3 import env
from july3.rule import Rule
from july3.util import render_percent_template, sh


class TemplateRendered(Rule):
    def __init__(self, target, source, render_fn=render_percent_template, sudo=False, dependencies=None):
        self.source = source
        self.render_fn = render_fn
        self.sudo = sudo
        super().__init__(target, dependencies=[source] + (dependencies or []))

    @staticmethod
    def command(self):
        self.render_fn(self.source, self.target, env, sudo=self.sudo)


class Directory(Rule):
    def __init__(self, target, sudo=False, dependencies=None):
        self.sudo = sudo
        super().__init__(target, dependencies=dependencies)

    @staticmethod
    def command(self):
        if not os.path.exists(self.target):
            os.makedirs(self.target)


class CommandRule(Rule):
    def __init__(self, command, sudo=False, dependencies=None):
        self.sudo = sudo
        super().__init__(command, dependencies=dependencies)

    def is_made(self):
        return sh(f'type {self.target}').returncode == 0

    def updated(self):
        return 0
