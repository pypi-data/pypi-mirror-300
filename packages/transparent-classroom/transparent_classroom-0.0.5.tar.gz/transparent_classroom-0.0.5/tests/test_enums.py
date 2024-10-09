import unittest
from enum import Enum
from typing import Type
from transparent_classroom.api import enums


class TestEnumeration(unittest.TestCase):
    """
    Test Enumerations Class

    Test class for validating the enumerations are set to the proper values. This
    class is mainly in place for enforcing code coverage.

    Attributes:


    """

    def __check_one_to_one_enums(self, cls: Type[Enum]) -> None:
        """
        Check that the name/values of the enum class are 1-to-1.

        :param cls: Type[Enum], The enumerated class to validate.
        :return: None

        """

        for item in cls:
            self.assertEqual(item.name, item.value)

    def __check_one_to_one_enums_case_insensitive(self, cls: Type[Enum]) -> None:
        """
        Check that the name/values of the enum class are 1-to-1 (case-insensitive).

        :param cls: Type[Enum], The enumerated class to validate.
        :return: None

        """

        for item in cls:
            self.assertEqual(item.name.upper(), item.value.upper())

    def __check_all_caps(self, value: str) -> None:
        """
        Check that value is all caps.

        :param value: str, The value to check.
        :return: None

        """

        self.assertEqual(value, value.upper())

    def __check_names_all_upper(self, cls: Type[Enum]) -> None:
        """
        Check that the names of the enum class items are all exclusively uppercase.

        :param cls: Type[Enum], The enumerated class to validate.
        :return: None

        """

        for item in cls:
            self.__check_all_caps(item.name)

    def __check_values_all_lower(self, cls: Type[Enum]) -> None:
        """
        Check that the names of the enum class items are all exclusively lowercase.

        :param cls: Type[Enum], The enumerated class to validate.
        :return: None

        """

        for item in cls:
            self.__check_all_caps(item.name)

    def test_model_types(self) -> None:
        """
        Test the ModelType Enumerated Class

        :return: None

        """

        self.__check_names_all_upper(cls=enums.ModelType)
        self.__check_values_all_lower(cls=enums.ModelType)
        self.__check_one_to_one_enums_case_insensitive(cls=enums.ModelType)

    def test_endpoint_behaviors(self) -> None:
        """
        Test the EndpointBehavior Enumerated Class

        :return: None

        """

        self.__check_names_all_upper(cls=enums.EndpointBehavior)
        self.__check_one_to_one_enums(cls=enums.EndpointBehavior)

    def test_http_methods(self) -> None:
        """
        Test the HTTPMethod Enumerated Class

        :return: None

        """

        self.__check_names_all_upper(cls=enums.HTTPMethod)
        self.__check_one_to_one_enums(cls=enums.HTTPMethod)


if __name__ == '__main__':
    unittest.main()
