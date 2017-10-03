"""Implementation of treadmill-admin CLI plugin.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging
import pkgutil

import click
import dns.exception  # pylint: disable=E0611
import dns.resolver
import kazoo
import kazoo.exceptions
import ldap3

from treadmill import restclient
from treadmill import cli
from treadmill import context


__path__ = pkgutil.extend_path(__path__, __name__)


def _handle_no_such_ldap_obj(err):
    """Handle LDAPNoSuchObjectResult exception."""
    if err.dn.find('ou=cells') != -1:
        rsrc_type = 'cell'
    elif err.dn.find('ou=allocations') != -1:
        rsrc_type = 'allocation'
    elif err.dn.find('ou=apps') != -1:
        rsrc_type = 'app'
    elif err.dn.find('ou=dns-servers') != -1:
        rsrc_type = 'dns configuration'
    else:
        rsrc_type = None

    if rsrc_type is None:
        rsrc_type = 'resource [%s]' % err.dn
    click.echo('Error: %s does not exist.' % rsrc_type, err=True)


ON_EXCEPTIONS = cli.handle_exceptions([
    (ldap3.LDAPInsufficientAccessRightsResult, 'Error: access denied.'),
    (ldap3.LDAPBindError, 'Error: invalid credentials.'),
    (ldap3.LDAPNoSuchObjectResult, _handle_no_such_ldap_obj),
    (kazoo.exceptions.NoAuthError, 'Error: not authorized.'),
    (kazoo.exceptions.NoNodeError, 'Error: resource does not exist.'),
    (restclient.NotAuthorizedError, restclient.handle_not_authorized),
    (restclient.MaxRequestRetriesError, None),
    (dns.exception.Timeout, 'Error: DNS server timeout.'),
    (dns.resolver.NXDOMAIN, 'Error: Could not resolve DNS record.'),
    (dns.resolver.YXDOMAIN, 'Error: DNS error.'),
    (context.ContextError, None),
])


def init():
    """Return top level command handler."""

    @click.group(cls=cli.make_commands(__name__))
    @click.pass_context
    def run(ctx):
        """Admin commands."""
        cli.init_logger('admin.conf')

        log_level = logging.WARN
        if ctx.obj.get('logging.debug'):
            log_level = logging.DEBUG

        logging.getLogger('treadmill').setLevel(log_level)
        logging.getLogger().setLevel(log_level)

    return run
