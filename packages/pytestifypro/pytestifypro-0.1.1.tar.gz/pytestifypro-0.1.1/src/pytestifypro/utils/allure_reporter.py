# src/pytestifypro/utils/allure_reporter.py

import allure


class AllureReporter:
    @staticmethod
    def add_feature(feature_name: str):
        """
        Add a feature to the Allure report.
        """
        allure.dynamic.feature(feature_name)

    @staticmethod
    def add_story(story_name: str):
        """
        Add a story to the Allure report.
        """
        allure.dynamic.story(story_name)

    @staticmethod
    def add_description(description: str):
        """
        Add a description to the Allure report.
        """
        allure.dynamic.description(description)

    @staticmethod
    def add_severity(severity_level: str):
        """
        Add a severity level to the Allure report.
        """
        allure.dynamic.severity(severity_level)

    @staticmethod
    def attach_file(name: str, content: bytes, attachment_type=allure.attachment_type.TEXT):
        """
        Attach a file to the Allure report.
        """
        allure.attach(name=name, body=content, attachment_type=attachment_type)

    @staticmethod
    def add_step(step_name: str):
        """
        Add a step to the Allure report.
        """
        with allure.step(step_name):
            pass
