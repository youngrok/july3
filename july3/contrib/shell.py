import time
from july3.rule import CallableTargetRule
from july3.util import sh


class ShellExitSuccessfulRule(CallableTargetRule):
    def is_made(self):
        p = sh(self.target, capture=True)
        self.executed = time.time()
        return p.returncode == 0

    def updated(self):
        return getattr(self, 'executed', 0)
