import unittest
from typing import Dict
from datetime import datetime
from transparent_classroom import models
from transparent_classroom.models import deserializers


class DeserializationTestCase(object):
    """
    Deserialization Test Case Class

    Attributes:
        data (`Dict`): The data to deserialize in an object.
        is_valid (`bool`): Flag indicating whether the test case data represents a valid
            deserialization of an object.

    """

    def __init__(self, data: Dict, is_valid: bool = True) -> None:
        """
        Test Case Constructor

        :param data: Dict, The data to deserialize in an object.
        :param is_valid: bool, Flag indicating whether the test case data represents a valid
            deserialization of an object.
        :return: None

        """

        self.data = data
        self.is_valid = is_valid

    @property
    def data(self) -> Dict:
        """
        The data to deserialize in an object.

        :return: Dict

        """

        return self._data

    @data.setter
    def data(self, value: Dict) -> None:
        """
        Set the data to deserialize in an object.

        :param value: Dict, The data to deserialize in an object.
        :return: None

        """

        self._data = value

    @property
    def is_valid(self) -> bool:
        """
        Flag indicating whether the test case data represents a valid deserialization
        of an object.

        :return: bool

        """

        return self._is_valid

    @is_valid.setter
    def is_valid(self, value: bool) -> None:
        """
        Set the flag indicating whether the test case data represents a valid
        deserialization of an object.

        :param value: bool, The flag indicating whether the test case data represents
            a valid deserialization of an object.
        :return: None

        """

        self._is_valid = value


class TestDeserializer(unittest.TestCase):
    """
    Test Deserializer Class

    Test class for testing the expected behavior of the deserializer object(s).

    Attributes:


    """

    """
    The test cases to check against the validator.

    """
    test_cases = [
        DeserializationTestCase(
            data={
                "id": 1
            }
        )
    ]

    """
    The deserializer to test.

    """
    deserializer = deserializers.Deserializer(cls=models.Model)

    def __test(self, model: models.Model, test_case: DeserializationTestCase) -> None:
        for k, v in vars(model).items():
            k = k.lstrip("_")

            if isinstance(v, models.Model):
                for k2, v2 in vars(v).items():
                    k2 = k2.lstrip("_")

                    if k2 in test_case.data.keys():
                        self.assertEqual(test_case.data[k2], v2)
            else:
                if k in test_case.data.keys():
                    self.assertEqual(test_case.data[k], v)
                elif "fields" in test_case.data.keys():
                    if isinstance(test_case.data["fields"], dict) and (k in test_case.data["fields"].keys()):
                        self.assertEqual(test_case.data["fields"][k], v)

    def test_deserialize(self) -> None:
        """
        Test deserializing the provided data into an object.

        :return: None

        """

        for test_case in self.test_cases:
            if test_case.is_valid:
                model = self.deserializer.deserialize(data=test_case.data)
                self.__test(model=model, test_case=test_case)
            else:
                self.assertRaises(ValueError, self.deserializer.deserialize, {"data": test_case.data})

    def test_deserialize_batch(self) -> None:
        """
        Test deserializing the list of entities into objects.

        :return: None

        """

        data = [test_case.data for test_case in self.test_cases]
        models = self.deserializer.batch(data=data)

        for i in range(0, len(models)):
            self.__test(model=models[i], test_case=self.test_cases[i])


class TestAuthDeserializer(TestDeserializer):
    """
    Test Auth Deserializer Class

    Test class for testing the expected behavior of the auth deserializer object.

    Attributes:


    """

    def setUp(self) -> None:
        """
        Set up the data to test the auth deserializer with.

        :return: None

        """

        self.test_cases = [
            DeserializationTestCase(
                data={
                    'type': 'user',
                    'id': 1,
                    'first_name': 'Hello',
                    'last_name': 'World',
                    'email': 'hello.world@test.edu',
                    'roles': ['teacher'],
                    "school_id": 1,
                    "api_token": "foo",
                    "push_tokens": [],
                    "push_enabled": False
                }
            )
        ]
        self.deserializer = deserializers.AuthDeserializer()


class TestActivityDeserializer(TestDeserializer):
    """
    Test Activity Deserializer Class

    Test class for testing the expected behavior of the activity deserializer object.

    Attributes:


    """

    def setUp(self) -> None:
        """
        Set up the data to test the auth deserializer with.

        :return: None

        """

        self.test_cases = [
            DeserializationTestCase(
                data={
                    "id": 1,
                    "author_id": 1,
                    "classroom_id": 1,
                    "text": "Hello, World!",
                    "html": "<h1>Hello, World!</h1>",
                    "date": datetime.today().date(),
                    "staff_unprocessed": True,
                    "photo_url": "https://www.hello.world/photo",
                    "medium_photo_url": "https://www.hello.world/medium-photo",
                    "large_photo_url": "https://www.hello.world/large-photo",
                    "original_photo_url": "https://www.hello.world/original-photo",
                    "created_at": datetime.now()
                }
            )
        ]
        self.deserializer = deserializers.ActivityDeserializer()


class TestChildDeserializer(TestDeserializer):
    """
    Test Child Deserializer Class

    Test class for testing the expected behavior of the child deserializer object.

    Attributes:


    """

    def setUp(self) -> None:
        """
        Set up the data to test the auth deserializer with.

        :return: None

        """

        self.test_cases = [
            DeserializationTestCase(
                data={
                    "id": 1,
                    "first_name": "Hello",
                    "middle_name": "Kind",
                    "last_name": "World",
                    "birth_date": datetime.today().date(),
                    "gender": "M",
                    "profile_photo": None,
                    "program": "Elementary",
                    "ethnicity": "White",
                    "household_income": "low",
                    "dominant_language": "English",
                    "grade": "2nd",
                    "student_id": "1",
                    "hours_string": "8:00AM(8:15AM) - 3:00PM M-F",
                    "allergies": None,
                    "notes": "Too cool for school",
                    "first_day": datetime.today().date(),
                    "last_day": datetime.today().date(),
                    "exit_notes": None,
                    "exit_reason": None,
                    "exit_survey_id": None,
                    "approved_adults_string": "Mr. and Mrs. Test",
                    "emergency_contacts_string": "Mr. and Mrs. Test",
                    "parent_ids": [1, 2],
                    "classroom_ids": [1, 2]
                }
            )
        ]
        self.deserializer = deserializers.ChildDeserializer()


class TestClassroomDeserializer(TestDeserializer):
    """
    Test Classroom Deserializer Class

    Test class for testing the expected behavior of the classroom deserializer object.

    Attributes:


    """

    def setUp(self) -> None:
        """
        Set up the data to test the auth deserializer with.

        :return: None

        """

        self.test_cases = [
            DeserializationTestCase(
                data={
                    "id": 1,
                    "name": "Hello",
                    "lesson_set_id": 1,
                    "level": "1st Grade",
                    "active": True
                }
            )
        ]
        self.deserializer = deserializers.ClassroomDeserializer()


class TestConferenceReportDeserializer(TestDeserializer):
    """
    Test Conference Report Deserializer Class

    Test class for testing the expected behavior of the conference report deserializer object.

    Attributes:


    """

    def setUp(self) -> None:
        """
        Set up the data to test the conference report deserializer with.

        :return: None

        """

        self.test_cases = [
            DeserializationTestCase(
                data={
                    "id": 1,
                    "name": "Hello",
                    "child_id": 1,
                    "data": [{

                    }]
                }
            )
        ]
        self.deserializer = deserializers.ConferenceReportDeserializer()


class TestEventDeserializer(TestDeserializer):
    """
    Test Event Deserializer Class

    Test class for testing the expected behavior of the event deserializer object.

    Attributes:


    """

    def setUp(self) -> None:
        """
        Set up the data to test the event deserializer with.

        :return: None

        """

        self.test_cases = [
            DeserializationTestCase(
                data={
                    "id": 1,
                    "classroom_id": 1,
                    "child_id": 1,
                    "event_type": "Hello",
                    "value": "World",
                    "created_by_id": 1,
                    "value2": "World",
                    "created_by_name": "Hello, World!",
                    "time": datetime.now()
                }
            )
        ]
        self.deserializer = deserializers.EventDeserializer()


class TestFormDeserializer(TestDeserializer):
    """
    Test Form Deserializer Class

    Test class for testing the expected behavior of the form deserializer object.

    Attributes:


    """

    def setUp(self) -> None:
        """
        Set up the data to test the form deserializer with.

        :return: None

        """

        self.test_cases = [
            DeserializationTestCase(
                data={
                    "id": 1,
                    "form_template_id": 1,
                    "state": "submitted",
                    "child_id": 1,
                    "created_at": datetime.now(),
                    "fields": {
                        "Student Name.first": "Hello",
                        "Student Name.last": "World",
                        "Parent Name": "Hello, World!",
                        "Classroom": "Archipelago",
                        "Photo and Documentation Release ": "yes, yes, yes",
                        "Signature": "Hello World"
                    }
                }
            )
        ]
        self.deserializer = deserializers.FormDeserializer()


class TestFormTemplateDeserializer(TestDeserializer):
    """
    Test Form Template Deserializer Class

    Test class for testing the expected behavior of the form template deserializer object.

    Attributes:


    """

    def setUp(self) -> None:
        """
        Set up the data to test the form template deserializer with.

        :return: None

        """

        self.test_cases = [
            DeserializationTestCase(
                data={
                    "id": 1,
                    "name": "Hello, World!",
                    "widgets": []
                }
            )
        ]
        self.deserializer = deserializers.FormTemplateDeserializer()


class TestLessonSetDeserializer(TestDeserializer):
    """
    Test Lesson Set Deserializer Class

    Test class for testing the expected behavior of the lesson set deserializer object.

    Attributes:


    """

    def setUp(self) -> None:
        """
        Set up the data to test the lesson set deserializer with.

        :return: None

        """

        self.test_cases = [
            DeserializationTestCase(
                data={
                    "id": 1,
                    "name": "Hello, World!",
                    "children": []
                }
            )
        ]
        self.deserializer = deserializers.LessonSetDeserializer()


class TestLevelDeserializer(TestDeserializer):
    """
    Test Level Deserializer Class

    Test class for testing the expected behavior of the level deserializer object.

    Attributes:


    """

    def setUp(self) -> None:
        """
        Set up the data to test the level deserializer with.

        :return: None

        """

        self.test_cases = [
            DeserializationTestCase(
                data={
                    "id": 1,
                    "child_id": 1,
                    "lesson_id": 1,
                    "proficiency": 3,
                    "date": datetime.today().date(),
                    "planned": True
                }
            )
        ]
        self.deserializer = deserializers.LevelDeserializer()


class TestOnlineApplicationDeserializer(TestDeserializer):
    """
    Test Online Application Deserializer Class

    Test class for testing the expected behavior of the online application deserializer object.

    Attributes:


    """

    def setUp(self) -> None:
        """
        Set up the data to test the online application deserializer with.

        :return: None

        """

        self.test_cases = [
            DeserializationTestCase(
                data={
                    "id": 1,
                    "school_id": 1,
                    "state": "accepted",
                    "fields": {
                        "program": "Elementary",
                        "child_name.first": "Hello",
                        "child_name.last": "World",
                        "child_birth_date": datetime.today().date(),
                        "child_gender": "M",
                        "mother_email": "hello@world.com",
                        "session_id": 1
                    }
                }
            )
        ]
        self.deserializer = deserializers.OnlineApplicationDeserializer()


class TestSchoolDeserializer(TestDeserializer):
    """
    Test School Deserializer Class

    Test class for testing the expected behavior of the school deserializer object.

    Attributes:


    """

    def setUp(self) -> None:
        """
        Set up the data to test the school deserializer with.

        :return: None

        """

        self.test_cases = [
            DeserializationTestCase(
                data={
                    "id": 1,
                    "name": "Hello, World!",
                    "phone": "(XXX) XXX-XXXX",
                    "address": "123 Hello World Lane",
                    "type": "network",
                    "timezone": "Pacific Time (US & Canada)"
                }
            )
        ]
        self.deserializer = deserializers.SchoolDeserializer()


class TestSessionDeserializer(TestDeserializer):
    """
    Test Session Deserializer Class

    Test class for testing the expected behavior of the session deserializer object.

    Attributes:


    """

    def setUp(self) -> None:
        """
        Set up the data to test the session deserializer with.

        :return: None

        """

        self.test_cases = [
            DeserializationTestCase(
                data={
                    "id": 1,
                    "name": "Hello World",
                    "start_date": datetime.today().date(),
                    "stop_date": datetime.today().date(),
                    "children": 100,
                    "current": True,
                    "inactive": False
                }
            )
        ]
        self.deserializer = deserializers.SessionDeserializer()


class TestUserDeserializer(TestDeserializer):
    """
    Test User Deserializer Class

    Test class for testing the expected behavior of the user deserializer object.

    Attributes:


    """

    def setUp(self) -> None:
        """
        Set up the data to test the user deserializer with.

        :return: None

        """

        self.test_cases = [
            DeserializationTestCase(
                data={
                    "id": 1,
                    "type": "user",
                    "inactive": False,
                    "email": "hello@world.com",
                    "first_name": "Hello",
                    "last_name": "World",
                    "roles": ["teacher"],
                    "accessible_classroom_ids": [1],
                    "default_classroom_id": 1,
                    "street": "123 Hello World Lane",
                    "postal_code": "11111",
                    "city": "Madison",
                    "state_province": "WI",
                    "home_number": "(XXX) XXX-XXXX",
                    "mobile_number": "(XXX) XXX-XXXX",
                    "work_number": "(XXX) XXX-XXXX"
                }
            )
        ]
        self.deserializer = deserializers.UserDeserializer()


if __name__ == '__main__':
    unittest.main()
