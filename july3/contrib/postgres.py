from july3 import env
from july3.rule import Rule
from july3.util import sh


class PostgresUser(Rule):

    def __init__(self, user, password, password_encrypted=False, superuser=False, dependencies=None):
        self.user = user
        self.password = password
        self.password_encrypted = password_encrypted
        self.superuser = superuser
        super().__init__('postgresuser:%s' % (self.user, ), dependencies)

    def is_made(self):
        return psql("SELECT COUNT(*) FROM pg_user WHERE usename = '%s';" % self.user, '-t -A', capture=True).strip() != '0'

    def updated(self):
        return 0

    @staticmethod
    def command(rule):
        options = [
            'SUPERUSER' if rule.superuser else 'NOSUPERUSER',
            'INHERIT',
            'LOGIN',
            "%s PASSWORD '%s'" % ('ENCRYPTED' if rule.password_encrypted else 'UNENCRYPTED', rule.password)
        ]
        psql("CREATE USER %s %s;" % (rule.user, ' '.join(options)))


class PostgresDatabase(Rule):

    def __init__(self, dbname, user, password, dependencies=None):
        self.dbname = dbname
        self.user = user
        self.password = password
        super().__init__('postgresdb:%s/%s' % (self.dbname, self.user), dependencies)

    def is_made(self):
        return psql(r'\l %s' % self.dbname, '-t -A', capture=True)

    def updated(self):
        return 0

    @staticmethod
    def command(rule):

        cmd = 'createdb --owner {owner} --template {template} --encoding={encoding} --lc-ctype={locale} --lc-collate={locale} {name}'.format(
            owner=rule.user,
            name=rule.dbname,
            template=env.get('postgres_template', 'template0'),
            encoding=env.get('postgres_encoding', 'UTF8'),
            locale=env.get('postgres_locale', 'en_US.UTF-8'),
        )

        if 'psql_sudo' in env:
            cmd = 'sudo -u {0} '.format(env.psql_sudo) + cmd

        sh(cmd)


class PostgresConnection(PostgresDatabase):
    def __init__(self, dbname, user, password, password_encrypted=False, superuser=False, dependencies=None):
        self.postgres_user = PostgresUser(user, password, password_encrypted, superuser)
        if not dependencies:
            dependencies = []

        dependencies.append(self.postgres_user)

        super().__init__(dbname, user, password, dependencies)
        self.name = 'postgres:%s/%s' % (dbname, user)


def psql(query, options='', capture=False):
    command = 'psql postgres %s -c "%s"' % (options, query)

    if 'psql_sudo' in env:
        command = 'sudo -u {0} '.format(env.psql_sudo) + command

    return sh(command, capture=capture).stdout