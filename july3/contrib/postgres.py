from july3 import env
from july3.rule import Rule, Target
from july3.util import sh


class PostgresUser(Rule):

    def __init__(self, user, password, password_encrypted=False, superuser=False, dependencies=None):
        super().__init__('postgresuser:%s' % (user, ), dependencies)
        self.target = Target(f"SELECT COUNT(*) FROM pg_user WHERE usename = '{user}';", lambda name: int(psql(name, '-t -A', capture=True)))
        self.user = user
        self.password = password
        self.password_encrypted = password_encrypted
        self.superuser = superuser

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
        super().__init__(f'postgresdb:{dbname}/{user}', dependencies)
        self.target = Target(r'\l %s' % dbname, lambda name: psql(name, '-t -A', capture=True))
        self.dbname = dbname
        self.user = user
        self.password = password

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