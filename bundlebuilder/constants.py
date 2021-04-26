SCHEMA_VERSION = '1.0.17'

# Default session configuration.

DEFAULT_SESSION_EXTERNAL_ID_PREFIX = 'ctim-bundle-builder'

DEFAULT_SESSION_SOURCE = 'SecureX Threat Response CTIM Bundle Builder'

DEFAULT_SESSION_SOURCE_URI = (
    'https://github.com/CiscoSecurity/tr-05-ctim-bundle-builder'
)

# Restrictions on fields of CTIM entities.

BOOLEAN_OPERATOR_CHOICES = (
    'and',
    'not',
    'or',
)

COLUMN_TYPE_CHOICES = (
    'integer',
    'markdown',
    'number',
    'observable',
    'string',
    'url',
)

CONFIDENCE_CHOICES = (
    'High',
    'Info',
    'Low',
    'Medium',
    'None',
    'Unknown',
)

COUNT_MIN_VALUE = 0

DESCRIPTION_MAX_LENGTH = 5000

DISPOSITION_MAP = {
    1: 'Clean',
    2: 'Malicious',
    3: 'Suspicious',
    4: 'Common',
    5: 'Unknown',
}

INDICATOR_TYPE_CHOICES = (
    'Anonymization',
    'C2',
    'Compromised PKI Certificate',
    'Domain Watchlist',
    'Exfiltration',
    'File Hash Watchlist',
    'Host Characteristics',
    'IMEI Watchlist',
    'IMSI Watchlist',
    'IP Watchlist',
    'Login Name',
    'Malicious E-mail',
    'Malware Artifacts',
    'Private Threat Feed',
    'URL Watchlist',
)

LANGUAGE_MAX_LENGTH = 1024

LIKELY_IMPACT_MAX_LENGTH = 5000

OBSERVABLE_TYPE_CHOICES = (
    'amp_computer_guid',
    'certificate_common_name',
    'certificate_issuer',
    'certificate_serial',
    'cisco_mid',
    'device',
    'domain',
    'email',
    'email_messageid',
    'email_subject',
    'file_name',
    'file_path',
    'hostname',
    'imei',
    'imsi',
    'ip',
    'ipv6',
    'mac_address',
    'md5',
    'ms_machine_id',
    'mutex',
    'ngfw_id',
    'ngfw_name',
    'odns_identity',
    'odns_identity_label',
    'orbital_node_id',
    'pki_serial',
    'process_name',
    'registry_key',
    'registry_name',
    'registry_path',
    's1_agent_id',
    'sha1',
    'sha256',
    'url',
    'user',
    'user_agent',
)

PRODUCER_MAX_LENGTH = 1024

PRIORITY_MIN_VALUE = 0
PRIORITY_MAX_VALUE = 100

REASON_MAX_LENGTH = 1024

REVISION_MIN_VALUE = 0

SEVERITY_CHOICES = (
    'High',
    'Info',
    'Low',
    'Medium',
    'None',
    'Unknown',
)

SHORT_DESCRIPTION_LENGTH = 2048

SOURCE_MAX_LENGTH = 2048

SOURCE_NAME_MAX_LENGTH = 2048

TAG_MAX_LENGTH = 1024

TEST_MECHANISM_MAX_LENGTH = 2048

TITLE_MAX_LENGTH = 1024

TLP_CHOICES = (
    'amber',
    'green',
    'red',
    'white',
)
