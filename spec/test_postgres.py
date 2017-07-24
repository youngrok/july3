import os
import unittest

from july3.contrib.postgres import PostgresUser, PostgresDatabase, PostgresConnection
from july3.util import sh


class TestPostgresRule(unittest.TestCase):

    def tearDown(self):
        sh('dropdb j3db', capture=True)
        sh('psql postgres -c "DROP USER j3test"', capture=True)

    def test_postgres_user_and_db(self):
        print('begin')

        postgres_user = PostgresUser('j3test', 'j3pass')
        postgres_db = PostgresDatabase('j3db', 'j3test', 'j3pass', dependencies=[postgres_user])

        postgres_db.make()
        self.assertEqual('1', sh(r'psql -U j3test j3db -t -c "select 1"', capture=True).stdout.strip())

        self.assertTrue(postgres_db.is_made())

    def test_postgres_connection(self):

        postgres = PostgresConnection('j3db', 'j3test', 'j3pass')

        postgres.make()

        sh(r'psql -U j3test j3db -t -c "select 1"')
        self.assertEqual('1', sh(r'psql -U j3test j3db -t -c "select 1"', capture=True).stdout.strip())

        self.assertTrue(postgres.is_made())
        postgres.make()

