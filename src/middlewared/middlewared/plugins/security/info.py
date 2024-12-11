from subprocess import run

from middlewared.api import api_method
from middlewared.api.current import (
    SystemSecurityFipsAvailableArgs, SystemSecurityFipsAvailableResult,
    SystemSecurityFipsEnabledArgs, SystemSecurityFipsEnabledResult,
)
from middlewared.service import CallError, Service


class SystemSecurityInfoService(Service):

    class Config:
        namespace = 'system.security.info'
        cli_namespace = 'system.security.info'

    @api_method(
        SystemSecurityFipsAvailableArgs, SystemSecurityFipsAvailableResult,
        roles=['SYSTEM_SECURITY_READ']
    )
    def fips_available(self):
        """Returns a boolean identifying whether or not FIPS
        mode may be toggled on this system"""
        # being able to toggle fips mode is hinged on whether
        # or not this is an iX licensed piece of hardware
        return bool(self.middleware.call_sync('system.license'))

    @api_method(
        SystemSecurityFipsEnabledArgs, SystemSecurityFipsEnabledResult,
        roles=['SYSTEM_SECURITY_READ']
    )
    def fips_enabled(self):
        """Returns a boolean identifying whether or not FIPS
        mode has been enabled on this system"""
        cp = run(['openssl', 'list', '-providers'], capture_output=True)
        if cp.returncode:
            raise CallError(f'Failed to determine if fips is enabled: {cp.stderr.decode()}')

        return b'OpenSSL FIPS Provider' in cp.stdout
