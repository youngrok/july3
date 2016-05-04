import os
import shutil
import unittest

from mako.template import Template

from july3 import env
from july3.target import NoTargetRuleSpecified, Target
from july3.contrib.python import PythonPackage
from july3.util import run


class TestFileTarget(unittest.TestCase):

    def setUp(self):
        env.build_path = 'test-build/'
        env.web_server_names = ['codeok.net']
        env.web_server_name = 'codeok.net'
        env.project_name = 'codeok'

    def tearDown(self):
        shutil.rmtree('test-build', ignore_errors=True)

    def test_file_depends_file(self):
        @Target('test-build/' + env.project_name, dependencies=['files/nginx-site.mako', 'test-build'])
        def nginx_site_file(target):
            with open(target.name, 'w') as f:
                f.write(Template(filename=target.dependencies[0]).render(**env))

        @Target('test-build')
        def build_dir(target):
            os.makedirs(target.name)

        nginx_site_file.make()
        self.assertTrue(env.web_server_name in open(env.build_path + env.project_name).read())

    def test_file_depends_non_existing_file(self):
        @Target('test-build/' + env.project_name + '.x', dependencies=['files/nginx-site.mako.x'])
        def nginx_site_file(rule):
            with open(rule.target.filename, 'w') as f:
                f.write(Template(filename=rule.dependencies[0]).render(**env))

        self.assertRaises(NoTargetRuleSpecified, nginx_site_file.make)


class TestNonFileTarget(unittest.TestCase):

    def setUp(self):
        env.build_path = 'test-build/'
        env.web_server_names = ['codeok.net']
        env.web_server_name = 'codeok.net'
        env.project_name = 'codeok'

    def tearDown(self):
        shutil.rmtree('test-build', ignore_errors=True)
        run('yes | pip uninstall toc')

    def test_non_file_target_rule(self):
        PythonPackage('toc').make()
        self.assertTrue('toc' in run('pip show toc', capture=True).stdout)

    def test_depend_non_file_target(self):

        os.makedirs('test-build')

        toc_install = PythonPackage('toc')

        @Target('test-build/' + env.project_name, dependencies=['files/nginx-site.mako', toc_install])
        def nginx_site_file(target):
            with open(target.name, 'w') as f:
                f.write(Template(filename=target.dependencies[0]).render(**env))


        nginx_site_file.make()

        self.assertTrue('toc' in run('pip show toc', capture=True).stdout)
        self.assertTrue(env.web_server_name in open(env.build_path + env.project_name).read())
