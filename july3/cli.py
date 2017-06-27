import inspect

import argh
from july3 import env
from july3.rule import rules, Rule


@argh.arg('--vars', nargs='*')
@argh.arg('--print-vars')
def make(*targets, **kwargs):
    for var in kwargs.get('vars') or []:
        k, v = var.split('=')
        env[k] = v

    if kwargs.get('print-vars'):
        print(env)

    if targets:
        for target in targets:
            rules.make(target)
    else:
        rules.make()


def main(rules_dict=None):
    if not rules_dict:
        caller_frame = inspect.stack()[1]
        rules_dict = dict(inspect.getmembers(inspect.getmodule(caller_frame[0])))

    for name, rule in rules_dict.items():
        if isinstance(rule, Rule):
            rules.register(name, rule)

    argh.dispatch_command(make)