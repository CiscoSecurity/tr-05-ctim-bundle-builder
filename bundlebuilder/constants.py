SCHEMA_VERSION = '1.0.14'

# Default session configuration.

DEFAULT_SESSION_EXTERNAL_ID_PREFIX = 'ctim-bundle-builder'

DEFAULT_SESSION_SOURCE = 'CTIM Bundle Builder'

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
    'URL Watchlist',
)

KILL_CHAIN_PHASE_NAME_CHOICES = (
    'actions-on-objective',
    'command-and-control',
    'delivery',
    'exploitation',
    'installation',
    'reconnaissance',
    'weaponization',
)

LANGUAGE_MAX_LENGTH = 1024

LIKELY_IMPACT_MAX_LENGTH = 5000

OBSERVABLE_TYPE_CHOICES = (
    'amp_computer_guid',
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
    'mutex',
    'ngfw_id',
    'ngfw_name',
    'odns_identity',
    'odns_identity_label',
    'pki_serial',
    'sha1',
    'sha256',
    'url',
    'user',
)

OBSERVABLE_RELATION_CHOICES = (
    'Allocated',
    'Allocated_By',
    'Attached_To',
    'Bound',
    'Bound_By',
    'Characterized_By',
    'Characterizes',
    'Child_Of',
    'Closed',
    'Closed_By',
    'Compressed',
    'Compressed_By',
    'Compressed_From',
    'Compressed_Into',
    'Connected_From',
    'Connected_To',
    'Contained_Within',
    'Contains',
    'Copied',
    'Copied_By',
    'Copied_From',
    'Copied_To',
    'Created',
    'Created_By',
    'Decoded',
    'Decoded_By',
    'Decompressed',
    'Decompressed_By',
    'Decrypted',
    'Decrypted_By',
    'Deleted',
    'Deleted_By',
    'Deleted_From',
    'Downloaded',
    'Downloaded_By',
    'Downloaded_From',
    'Downloaded_To',
    'Dropped',
    'Dropped_By',
    'Encoded',
    'Encoded_By',
    'Encrypted',
    'Encrypted_By',
    'Encrypted_From',
    'Encrypted_To',
    'Extracted_From',
    'FQDN_Of',
    'Freed',
    'Freed_By',
    'Hooked',
    'Hooked_By',
    'Initialized_By',
    'Initialized_To',
    'Injected',
    'Injected_As',
    'Injected_By',
    'Injected_Into',
    'Installed',
    'Installed_By',
    'Joined',
    'Joined_By',
    'Killed',
    'Killed_By',
    'Listened_On',
    'Listened_On_By',
    'Loaded_From',
    'Loaded_Into',
    'Locked',
    'Locked_By',
    'Mapped_By',
    'Mapped_Into',
    'Merged',
    'Merged_By',
    'Modified_Properties_Of',
    'Monitored',
    'Monitored_By',
    'Moved',
    'Moved_By',
    'Moved_From',
    'Moved_To',
    'Opened',
    'Opened_By',
    'Packed',
    'Packed_By',
    'Packed_From',
    'Packed_Into',
    'Parent_Of',
    'Paused',
    'Paused_By',
    'Previously_Contained',
    'Properties_Modified_By',
    'Properties_Queried',
    'Properties_Queried_By',
    'Read_From',
    'Read_From_By',
    'Received',
    'Received_By',
    'Received_From',
    'Received_Via_Upload',
    'Redirects_To',
    'Refers_To',
    'Related_To',
    'Renamed',
    'Renamed_By',
    'Renamed_From',
    'Renamed_To',
    'Resolved_To',
    'Resumed',
    'Resumed_By',
    'Root_Domain_Of',
    'Searched_For',
    'Searched_For_By',
    'Sent',
    'Sent_By',
    'Sent_To',
    'Sent_Via_Upload',
    'Set_From',
    'Set_To',
    'Sub-domain_Of',
    'Supra-domain_Of',
    'Suspended',
    'Suspended_By',
    'Unhooked',
    'Unhooked_By',
    'Unlocked',
    'Unlocked_By',
    'Unpacked',
    'Unpacked_By',
    'Uploaded',
    'Uploaded_By',
    'Uploaded_From',
    'Uploaded_To',
    'Used',
    'Used_By',
    'Values_Enumerated',
    'Values_Enumerated_By',
    'Written_To_By',
    'Wrote_To',
)

PRODUCER_MAX_LENGTH = 1024

PRIORITY_MIN_VALUE = 0
PRIORITY_MAX_VALUE = 100

REASON_MAX_LENGTH = 1024

RELATIONSHIP_TYPE_CHOICES = (
    'attributed-to',
    'based-on',
    'derived-from',
    'detects',
    'duplicate-of',
    'element-of',
    'exploits',
    'indicates',
    'member-of',
    'mitigates',
    'related-to',
    'sighting-of',
    'targets',
    'uses',
    'variant-of',
)

RESOLUTION_CHOICES = (
    'allowed',
    'blocked',
    'contained',
    'detected',
)

REVISION_MIN_VALUE = 0

SENSOR_CHOICES = (
    'endpoint',
    'endpoint.digital-telephone-handset',
    'endpoint.laptop',
    'endpoint.pos-terminal',
    'endpoint.printer',
    'endpoint.sensor',
    'endpoint.server',
    'endpoint.smart-meter',
    'endpoint.smart-phone',
    'endpoint.tablet',
    'endpoint.workstation',
    'network',
    'network.bridge',
    'network.firewall',
    'network.gateway',
    'network.guard',
    'network.hips',
    'network.hub',
    'network.ids',
    'network.ips',
    'network.modem',
    'network.nic',
    'network.proxy',
    'network.router',
    'network.security_manager',
    'network.sense_making',
    'network.sensor',
    'network.switch',
    'network.vpn',
    'network.wap',
    'process',
    'process.aaa-server',
    'process.anti-virus-scanner',
    'process.connection-scanner',
    'process.directory-service',
    'process.dns-server',
    'process.email-service',
    'process.file-scanner',
    'process.location-service',
    'process.network-scanner',
    'process.remediation-service',
    'process.reputation-service',
    'process.sandbox',
    'process.virtualization-service',
    'process.vulnerability-scanner',
)

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

SPECIFICATION_TYPE_CHOICES = (
    'Judgement',
    'ThreatBrain',
    'Snort',
    'SIOC',
    'OpenIOC',
)

TAG_MAX_LENGTH = 1024

TEST_MECHANISM_MAX_LENGTH = 2048

TITLE_MAX_LENGTH = 1024

TLP_CHOICES = (
    'amber',
    'green',
    'red',
    'white',
)
