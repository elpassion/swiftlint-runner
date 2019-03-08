
from setuptools import setup, find_packages
from slrunner.core.version import get_version

VERSION = get_version()

f = open('README.md', 'r')
LONG_DESCRIPTION = f.read()
f.close()

setup(
    name='slrunner',
    version=VERSION,
    description='Missing SwiftLint runner with ability to define config file per target',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    author='Jakub Turek',
    author_email='jakub.turek@elpassion.com',
    url='https://github.com/elpassion/swiftlint-runner',
    license='MIT',
    packages=find_packages(exclude=['ez_setup', 'tests*']),
    package_data={'slrunner': ['templates/*']},
    include_package_data=True,
    entry_points="""
        [console_scripts]
        slrunner = slrunner.main:main
    """,
)
