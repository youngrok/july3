import os
import shutil
import unittest

from mako.template import Template

from july3 import env
from july3.rule import NoCommandSpecified, Rule
from july3.contrib.python import PythonPackage
from july3.util import sh


class TestFileRule(unittest.TestCase):

    def setUp(self):
        env.build_path = 'test-build/'
        env.web_server_names = ['codeok.net']
        env.web_server_name = 'codeok.net'
        env.project_name = 'codeok'

    def tearDown(self):
        shutil.rmtree('test-build', ignore_errors=True)

    def test_file_depends_file(self):

        @Rule(f'test-build/{env.project_name}', dependencies=['files/nginx-site.mako', 'test-build'])
        def nginx_site_file(rule):
            with open(rule.target, 'w') as f:
                f.write(Template(filename=rule.dependencies[0]).render(**env))

        @Rule('test-build')
        def build_dir(rule):
            os.makedirs(rule.target)

        nginx_site_file.make()
        self.assertTrue(env.web_server_name in open(env.build_path + env.project_name).read())

    def test_file_depends_non_existing_file(self):
        @Rule(f'test-build/{env.project_name}.x', dependencies=['files/nginx-site.mako.x'])
        def nginx_site_file(rule):
            with open(rule.rule.filename, 'w') as f:
                f.write(Template(filename=rule.dependencies[0]).render(**env))

        self.assertRaises(NoCommandSpecified, nginx_site_file.make)


class TestNonFileRule(unittest.TestCase):

    def setUp(self):
        env.build_path = 'test-build/'
        env.web_server_names = ['codeok.net']
        env.web_server_name = 'codeok.net'
        env.project_name = 'codeok'

    def tearDown(self):
        shutil.rmtree('test-build', ignore_errors=True)
        sh('yes | pip uninstall toc')

    def test_non_file_rule(self):
        PythonPackage('toc').make()
        self.assertTrue('toc' in sh('pip show toc', capture=True).stdout)

    def test_depend_non_file_rule(self):

        os.makedirs('test-build')

        toc_install = PythonPackage('toc')

        @Rule(f'test-build/{env.project_name}', dependencies=['files/nginx-site.mako', toc_install])
        def nginx_site_file(rule):
            with open(rule.target, 'w') as f:
                f.write(Template(filename=rule.dependencies[0]).render(**env))


        nginx_site_file.make()

        self.assertTrue('toc' in sh('pip show toc', capture=True).stdout)
        self.assertTrue(env.web_server_name in open(env.build_path + env.project_name).read())
