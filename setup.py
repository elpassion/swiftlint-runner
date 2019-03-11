from setuptools import setup

setup(
    name='swiftlint-runner',
    version='0.1',
    packages=['commands', 'commands.utils'],
    url='https://github.com/elpassion/swiftlint-runner',
    license='MIT',
    author='Jakub Turek',
    author_email='jakub.turek@elpassion.pl',
    description='Missing SwiftLint runner with ability to define config file per target'
)
