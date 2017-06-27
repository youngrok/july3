import os


class TargetNotFound(Exception):
    pass


class RuleGraph:

    def __init__(self):
        self.rules = {}

    def register(self, name, rule):
        self.rules[name] = rule

    def find_rule(self, dependency):
        if isinstance(dependency, Rule):
            return dependency

        if dependency in self.rules:
            return self.rules[dependency]

        return Rule(dependency)

    def make(self, target_name=None):
        if not target_name:
            target_name = next(iter(self.rules.keys()))

        if target_name not in self.rules:
            target_names = '\n'.join([' - ' + k for k in self.rules.keys()])
            raise TargetNotFound(f'{target_name} not found.\nAvaiable targets:\n{target_names}')

        self.rules[target_name].make()


rules = RuleGraph()


class Rule:

    def __init__(self, target, dependencies=None, **options):
        self.target = target
        self.dependencies = dependencies if dependencies else []
        self.options = options
        rules.register(str(self.target), self)

    def make(self):
        need_update = False

        for d in self.dependencies:
            dependency_rule = rules.find_rule(d)
            dependency_rule.make()

            if dependency_rule.updated() > self.updated():
                need_update = True

        if not self.is_made():
            need_update = True

        if not need_update:
            return

        if not hasattr(self, 'command'):
            raise NoCommandSpecified('Rule:' + str(self.target))

        self.command(self)

    def __str__(self):
        return str(self.target)

    def __call__(self, command):
        self.command = command
        rules.register(command.__name__, self)
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

