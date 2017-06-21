import logging
import subprocess
from subprocess import CalledProcessError

import sys
from tempfile import NamedTemporaryFile


class ProcessResult:
    def __init__(self, stdout, stderr, returncode):
        self.stdout = stdout.strip().decode() if stdout else ''
        self.stderr = stderr.strip().decode() if stderr else ''
        self.returncode = returncode


def run(command, capture=False):
    if capture:
        return subprocess.run(command, shell=True, encoding='utf8', stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    print(command)
    return subprocess.run(command, shell=True)



def render_percent_template(filename, destination, context, sudo=False):
    with open(filename) as f:
        with NamedTemporaryFile('w') as output:
            output.write(f.read() % context)
            run(f'{sudo_cmd(sudo)} cp {output.name} {destination}')


def render_template(filename, destination, context, sudo=False):
    with open(filename) as f:
        with NamedTemporaryFile('w') as output:
            output.write(f.read().format_map(context))
            sudo_cmd = 'sudo' if sudo else ''
            run(f'{sudo_cmd(sudo)} cp {output.name} {destination}')


def sudo_cmd(user=None):
    if not user:
        return ''

    if user is True:
        return 'sudo '

    return f'sudo -u {user} '


def symlink(source, rule):
    run('sudo rm -f %s' % (rule,))
    run('sudo ln -s %s %s' % (source, rule))


