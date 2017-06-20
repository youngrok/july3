import os


rules = {}


class Rule:

    def __init__(self, target, dependencies=None):
        self.target = target
        self.dependencies = dependencies if dependencies else []

    def make(self):
        need_update = False

        for d in self.dependencies:
            dependency_rule = self.find_rule(d)
            dependency_rule.make()

            if dependency_rule.updated() > self.updated():
                need_update = True

        if not self.is_made():
            need_update = True

        if not need_update:
            return

        if not hasattr(self, 'command'):
            raise NoCommandSpecified(self.target)

        self.command(self)


    def find_rule(self, dependency):
        if isinstance(dependency, Rule):
            return dependency

        if dependency in rules:
            return rules[dependency]

        return Rule(dependency)

    def __str__(self):
        return self.target

    def __call__(self, command):
        self.command = command
        rules[str(self.target)] = self
        rules[command.__name__] = self
        return self

    def is_made(self):
        return os.path.exists(self.target)

    def updated(self):
        if self.is_made():
            return os.path.getmtime(self.target)

        return 0


class VirtualRule(Rule):

    def is_made(self):
        return False

    def updated(self):
        return 0


class NoCommandSpecified(Exception):
    pass

