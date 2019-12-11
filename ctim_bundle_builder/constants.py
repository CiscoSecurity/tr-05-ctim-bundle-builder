EXTERNAL_ID_PREFIX = 'ctim-bundle-builder'

# Restrictions on fields of CTIM entities.

DESCRIPTION_MAX_LENGTH = 5000

LANGUAGE_MAX_LENGTH = 1024

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

REVISION_MIN_VALUE = 0

SCHEMA_VERSION = '1.0.12'

SHORT_DESCRIPTION_LENGTH = 2048

SOURCE_MAX_LENGTH = 2048

SOURCE_NAME_MAX_LENGTH = 2048

TITLE_MAX_LENGTH = 1024

TLP_CHOICES = (
    'amber',
    'green',
    'red',
    'white',
)
