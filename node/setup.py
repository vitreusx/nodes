import setuptools
from pip._internal.req import parse_requirements

setuptools.setup(
    name = 'node',
    version = '0',
    author = 'aurora-team',
    description = 'A node deamon for the Aurora IO project.',
    url = 'https://gitlab.com/vitreus/io',
    packages = setuptools.find_packages(),
    install_requires = parse_requirements('requirements.txt', session='hack')
)
