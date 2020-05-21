import setuptools

setuptools.setup(
    name = 'node_cli',
    version = '0',
    author = 'aurora-team',
    description = 'A node CLI for the Aurora IO project.',
    url = 'https://gitlab.com/vitreus/io',
    packages = setuptools.find_packages(),
    install_requires = open('requirements.txt', 'r').read().splitlines()
)
