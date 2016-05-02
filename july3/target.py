import os

from july3 import rules


class Target:

    def __init__(self, name, dependencies=None):
        self.name = name
        self.dependencies = dependencies if dependencies else []

    def make(self):
        need_update = False

        for d in self.dependencies:
            dependency_rule = self.find_target(d)
            dependency_rule.make()

            if dependency_rule.updated() > self.updated():
                need_update = True

        if not self.is_made():
            need_update = True

        if not need_update:
            return

        if not hasattr(self, 'command'):
            raise NoTargetRuleSpecified(self.name)

        self.command(self)


    def find_target(self, dependency):
        if isinstance(dependency, Target):
            return dependency

        if dependency in rules:
            return rules[dependency]

        return Target(dependency)

    def __str__(self):
        return self.name

    def __call__(self, command):
        self.command = command
        rules[str(self.name)] = self
        rules[command.__name__] = self
        return self

    def is_made(self):
        return os.path.exists(self.name)

    def updated(self):
        if self.is_made():
            return os.path.getmtime(self.name)

        return 0


class NoTargetRuleSpecified(Exception):
    pass

