import os

from unittest import TestCase

from commands.utils.xcproj import list_swift_files


class XCProjTestCase(TestCase):
    def test_that_files_for_app_target_are_resolved(self):
        """
        Test that files for application target called TestProject are correctly resolved.
        """
        files = list_swift_files('tests/resources/TestProject/TestProject.xcodeproj', 'TestProject')

        absolute_file_path = 'tests/resources/TestProject/TestProject/SomeGroup/Deeply/Nested/TestAbsoluteFile.swift'

        self.assertEqual(set(files), {
            'tests/resources/TestProject/TestProject/SomeGroup/TestController.swift',
            os.path.join(os.getcwd(), absolute_file_path),
            'tests/resources/TestProject/TestProject/ViewController.swift',
            'tests/resources/TestProject/TestProject/AppDelegate.swift'
        })

    def test_that_files_for_framework_target_are_resolved(self):
        """
        Test that files for framework target called Framework are correctly resolved.
        """
        files = list_swift_files('tests/resources/TestProject/TestProject.xcodeproj', 'Framework')

        absolute_file_path = 'tests/resources/TestProject/TestProject/SomeGroup/Deeply/Nested/TestAbsoluteFile.swift'

        self.assertEqual(set(files), {
            'tests/resources/TestProject/TestProject/SomeGroup/TestController.swift',
            os.path.join(os.getcwd(), absolute_file_path),
        })
