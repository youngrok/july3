import logging
import subprocess
from subprocess import CalledProcessError

import sys


class ProcessResult:
    def __init__(self, stdout, stderr, returncode):
        self.stdout = stdout.strip().decode() if stdout else ''
        self.stderr = stderr.strip().decode() if stderr else ''
        self.returncode = returncode


def run(command, capture=False):
    print(command)
    p = subprocess.Popen(command,
                         shell=True,
                         stdout=subprocess.PIPE if capture else sys.stdout)

    (stdout, stderr) = p.communicate()

    if not capture and p.returncode != 0:
        raise CalledProcessError(p.returncode, command, stdout, stderr)

    return ProcessResult(stdout, stderr, p.returncode)


def render_template(source, target, context):
    with open(source) as s:
        with open(target, 'w') as t:
            t.write(s.read().format_map(context))


def symlink(source, target):
    run('sudo rm -f %s' % (target,))
    run('sudo ln -s %s %s' % (source, target))


