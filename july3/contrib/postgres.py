from july3 import env
from july3.target import Target
from july3.util import run


class PostgresUser(Target):

    def __init__(self, user, password, password_encrypted=False, superuser=False, dependencies=None):
        self.user = user
        self.password = password
        self.password_encrypted = password_encrypted
        self.superuser = superuser
        super().__init__('postgresuser:%s' % (self.user, ), dependencies)

    def is_made(self):
        return psql("SELECT COUNT(*) FROM pg_user WHERE usename = '%s';" % self.user, '-t -A') != '0'

    def updated(self):
        return 0

    @staticmethod
    def command(target):
        options = [
            'SUPERUSER' if target.superuser else 'NOSUPERUSER',
            'INHERIT',
            'LOGIN',
            "%s PASSWORD '%s'" % ('ENCRYPTED' if target.password_encrypted else 'UNENCRYPTED', target.password)
        ]

        psql("CREATE USER %s %s;" % (target.user, ' '.join(options)))


class PostgresDatabase(Target):

    def __init__(self, dbname, user, password, dependencies=None):
        self.dbname = dbname
        self.user = user
        self.password = password
        super().__init__('postgresdb:%s/%s' % (self.dbname, self.user), dependencies)

    def is_made(self):
        return psql(r'\l %s' % self.dbname, '-t -A')

    def updated(self):
        return 0

    @staticmethod
    def command(target):
        run('''createdb --owner %(owner)s --template %(template)s \
            --encoding=%(encoding)s --lc-ctype=%(locale)s \
            --lc-collate=%(locale)s %(name)s''' % {
            'owner': target.user,
            'name': target.dbname,
            'template': env.get('postgres_template', 'template0'),
            'encoding': env.get('postgres_encoding', 'UTF8'),
            'locale': env.get('postgres_locale', 'en_US.UTF-8'),
        })


class PostgresConnection(PostgresDatabase):
    def __init__(self, dbname, user, password, password_encrypted=False, superuser=False, dependencies=None):
        self.postgres_user = PostgresUser(user, password, password_encrypted, superuser)
        if not dependencies:
            dependencies = []

        dependencies.append(self.postgres_user)

        super().__init__(dbname, user, password, dependencies)
        self.name = 'postgres:%s/%s' % (dbname, user)


def psql(query, options=''):
    command = 'psql postgres %s -c "%s"' % (options, query)
    return run(command).stdout