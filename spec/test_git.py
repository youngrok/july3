import os
import shutil
import unittest

from july3 import env
from july3.contrib.git import GitPull
from july3.rule import Rule


class TestGit(unittest.TestCase):

    def tearDown(self):
        shutil.rmtree('test-build', ignore_errors=True)

    def test_updated(self):
        env.deploy_key_file = '~/.ssh/id_rsa'

        @Rule('test-build')
        def build_dir(rule):
            os.makedirs(rule.target)

        source_update = GitPull('git@github.com:youngrok/july3.git', 'test-build/july3', dependencies=[build_dir])
        source_update.make()

        self.assertTrue(os.path.exists('test-build/july3/setup.py'))


