import os
from shutil import copyfile

from unittest import TestCase
from unittest.mock import patch

import yaml
from click.testing import CliRunner

from commands.lint import lint


class LintTestCase(TestCase):
    def setUp(self):
        self.runner = CliRunner()

    @patch('commands.lint.list_swift_files')
    @patch('commands.lint.run')
    def test_that_linting_invokes_listing_files_with_correct_arguments(self, _, list_files):
        """
        Test that linting invokes listing files with correct arguments.
        """
        list_files.return_value = []
        swiftlint_path = os.path.join(os.getcwd(), 'tests/resources/.swiftlint.yml')

        with self.runner.isolated_filesystem():
            copyfile(swiftlint_path, '.sources.yml')
            _ = self.runner.invoke(lint, ['path_to/Project.xcodeproj', 'SomeTarget', '.sources.yml'])

            list_files.assert_called_once_with('path_to/Project.xcodeproj', 'SomeTarget')

    @patch('commands.lint.list_swift_files')
    @patch('commands.lint.run')
    def test_that_linting_deletes_swiftlint_file(self, run, list_files):
        """
        Test that linting deletes SwiftLint file.
        """
        list_files.return_value = []
        run.return_value.returncode = 0
        swiftlint_path = os.path.join(os.getcwd(), 'tests/resources/.swiftlint.yml')

        with self.runner.isolated_filesystem():
            copyfile(swiftlint_path, '.sources.yml')
            runner = self.runner.invoke(lint, ['Project.xcodeproj', 'SomeTarget', '.sources.yml'])

            self.assertEqual(0, runner.exit_code)
            self.assertFalse(os.path.exists('.swiftlint.yml'))

    @patch('commands.lint.list_swift_files')
    @patch('commands.lint.run')
    def test_that_linting_appends_included_files_to_swiftlint_config(self, _, list_files):
        """
        Test that linting appends included files to SwiftLint config.
        """
        list_files.return_value = ['A', 'B', 'C']
        swiftlint_path = os.path.join(os.getcwd(), 'tests/resources/.swiftlint.yml')

        with self.runner.isolated_filesystem():
            copyfile(swiftlint_path, '.sources.yml')
            _ = self.runner.invoke(lint, ['Project.xcodeproj', 'SomeTarget', '.sources.yml', '--no-delete-config'])

            with open('.swiftlint.yml', 'r') as sources:
                sources = yaml.load(sources)

                self.assertIn('included', sources)
                self.assertEqual(sources['included'], ['A', 'B', 'C'])

    @patch('commands.lint.list_swift_files')
    @patch('commands.lint.run')
    def test_that_swiftlint_is_invoked(self, run, list_files):
        """
        Test that linting invokes SwiftLint.
        """
        list_files.return_value = ['A', 'B', 'C']
        run.return_value.returncode = -8
        swiftlint_path = os.path.join(os.getcwd(), 'tests/resources/.swiftlint.yml')

        with self.runner.isolated_filesystem():
            copyfile(swiftlint_path, '.sources.yml')
            result = self.runner.invoke(lint, ['Project.xcodeproj', 'SomeTarget', '.sources.yml'])

            run.assert_called_once_with(["swiftlint"])
            self.assertEqual(-8, result.exit_code)
