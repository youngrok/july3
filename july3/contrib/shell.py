import time
from july3.rule import CallableTargetRule, OnceRule
from july3.util import sh


class ShellExitSuccessfulRule(CallableTargetRule, OnceRule):
    def is_made(self):
        p = sh(self.target, capture=True)
        self.executed = time.time()
        return p.returncode == 0
