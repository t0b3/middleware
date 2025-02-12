import copy

from middlewared.plugins.crypto_.cert_profiles import CSR_PROFILES
from middlewared.plugins.crypto_.csr import generate_certificate_signing_request


CERT_BOT_EMAIL = 'cert-bot@ixsystems.com'


def get_hostnames_from_hostname_config(hostname_config: dict) -> list[str]:
    return [f'*.{hostname_config["base_domain"]}']


def generate_csr(hostnames: list[str]) -> (str, str):
    return generate_certificate_signing_request({
        'key_type': 'RSA',
        'key_length': 4096,
        'san': hostnames,
        'country': 'US',
        'state': 'TN',
        'city': 'Maryville',
        'organization': 'iX',
        'organizational_unit': 'TNC',
        'email': CERT_BOT_EMAIL,
        'digest_algorithm': 'SHA256',
        'cert_extensions': copy.deepcopy(CSR_PROFILES['HTTPS RSA Certificate']['cert_extensions']),
        # We do not specify a common as domain hostname is bigger then 64 chars and cryptography starts complaining
    })
