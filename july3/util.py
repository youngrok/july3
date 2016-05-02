import subprocess


class ProcessResult:
    def __init__(self, stdout, stderr, returncode):
        self.stdout = stdout.strip().decode() if stdout else ''
        self.stderr = stderr.strip().decode() if stderr else ''
        self.returncode = returncode


def run(command):
    p = subprocess.Popen(command,
                         shell=True,
                         stdout=subprocess.PIPE,
                         stdin=subprocess.PIPE)

    (stdout, stderr) = p.communicate()

    if stderr:
        print(stderr)
    else:
        stderr

    return ProcessResult(stdout, stderr, p.returncode)

    return out


def symlink(source, target):
    run('sudo rm -f %s' % (target,))
    run('sudo ln -s %s %s' % (source, target))


