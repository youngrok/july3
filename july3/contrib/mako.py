from tempfile import NamedTemporaryFile
from mako.template import Template

from july3.util import sh


def render_template(source, rule, context, sudo=False):
    with NamedTemporaryFile('w') as tmp:
        tmp.file.write(Template(filename=source).render(**context))
        tmp.file.flush()
        sudo_cmd = 'sudo ' if sudo else ''
        sh('%scp %s %s' % (sudo_cmd, tmp.name, rule))
        sh('%schmod a+r %s' % (sudo_cmd, rule, ))
