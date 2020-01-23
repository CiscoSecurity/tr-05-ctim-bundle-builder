import re
import setuptools


def read_version():
    with open('bundlebuilder/version.py', 'r') as fin:
        return re.search(
            r"^__version__ = '(?P<version>.+)'$",
            fin.read().strip(),
        ).group('version')


def read_requirements():
    with open('requirements.txt', 'r') as fin:
        requirements = []
        for line in fin:
            # Discard any comments (i.e. everything after the very first '#').
            line = line.split('#', 1)[0].strip()
            if line:
                requirements.append(line)
        return requirements


NAME = 'bundlebuilder'

DESCRIPTION = 'Python CTIM Bundle Builder'

AUTHOR = 'Cisco Security'

URL = 'https://github.com/CiscoSecurity/tr-05-ctim-bundle-builder'

VERSION = read_version()

INSTALL_REQUIRES = read_requirements()

PACKAGES = setuptools.find_packages(exclude=['tests', 'tests.*'])

KEYWORDS = ['cisco', 'security', 'python', 'ctim', 'bundle', 'builder']

PYTHON_REQUIRES = '>=3.6'

CLASSIFIERS = [
    'Intended Audience :: Developers',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Topic :: Software Development :: Libraries :: Python Modules',
]

LICENSE = 'MIT'


setuptools.setup(
    name=NAME,
    description=DESCRIPTION,
    author=AUTHOR,
    url=URL,
    version=VERSION,
    install_requires=INSTALL_REQUIRES,
    packages=PACKAGES,
    keywords=KEYWORDS,
    python_requires=PYTHON_REQUIRES,
    classifiers=CLASSIFIERS,
    license=LICENSE,
)
