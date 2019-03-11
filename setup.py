import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name='swiftlint-runner',
    version='0.0.1',
    long_description=README,
    long_description_content_type='text/markdown',
    packages=['commands', 'commands.utils'],
    url='https://github.com/elpassion/swiftlint-runner',
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ],
    author='Jakub Turek',
    author_email='jakub.turek@elpassion.pl',
    description='Missing SwiftLint runner with ability to define config file per target',
    entry_points={
        "console_scripts": [
            "slrunner=commands.lint:lint",
        ]
    },
    install_requires=['click', 'pyyaml', 'mod-pbxproj']
)
