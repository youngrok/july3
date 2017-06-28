import os
import subprocess

from tempfile import NamedTemporaryFile

from contextlib import contextmanager


class ProcessResult:
    def __init__(self, stdout, stderr, returncode):
        self.stdout = stdout.strip().decode() if stdout else ''
        self.stderr = stderr.strip().decode() if stderr else ''
        self.returncode = returncode


def sh(command, capture=False, sudo=False):
    if capture:
        return subprocess.run(command, shell=True, encoding='utf8', stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    command = f'{sudo_cmd(sudo)} {command}'

    print(command)
    return subprocess.run(command, shell=True)



def render_percent_template(filename, destination, context, sudo=False):
    with open(filename) as f:
        with NamedTemporaryFile('w') as output:
            output.write(f.read() % context)
            output.flush()
            sh(f'{sudo_cmd(sudo)} cp {output.name} {destination}')


def render_template(filename, destination, context, sudo=False):
    with open(filename) as f:
        with NamedTemporaryFile('w') as output:
            output.write(f.read().format_map(context))
            output.flush()
            sh(f'{sudo_cmd(sudo)} cp {output.name} {destination}')


def sudo_cmd(user=None):
    if not user:
        return ''

    if user is True:
        return 'sudo '

    return f'sudo -u {user} '


def symlink(source, rule):
    sh('sudo rm -f %s' % (rule,))
    sh('sudo ln -s %s %s' % (source, rule))


@contextmanager
def cd(path):
    old = os.getcwd()
    os.chdir(path)
    yield
    os.chdir(old)