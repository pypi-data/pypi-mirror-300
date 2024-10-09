import unittest
from datetime import datetime
from transparent_classroom import models
from transparent_classroom.models.utilities import Formatter


class TestJSONModel(unittest.TestCase):
    """
    Test JSON Model Class

    Test class for validating the expected behavior of JSONModel objects.

    Attributes:


    """

    """
    The model type to test.
    
    """
    cls = models.Model

    """
    Data used for object initialization.

    """
    data = {
        "id": 1
    }

    def test_from_dict(self) -> None:
        """
        Test the from_dict method for JSON models

        :return: None

        """

        model = self.cls.from_dict(data=self.data)

        for k, v in self.data.items():
            self.assertEqual(v, model.__getattribute__(k))

    def test_to_dict(self) -> None:
        """
        Test the to_dict method for JSON models

        :return: None

        """

        model = self.cls.from_dict(data=self.data)
        data = model.to_dict()
        self.assertEqual(self.data, data)

    def test_to_json(self) -> None:
        """
        Test the to_json method for JSON models

        :return: None

        """

        model = self.cls.from_dict(data=self.data)
        data = model.to_json()
        self.assertEqual(Formatter.jsonify(self.data), data)


class TestAuthModel(TestJSONModel):
    """
    Test Auth Model Class

    Test class for validating the auth model class.

    Attributes:


    """

    def setUp(self) -> None:
        """
        Set up the data to test with for the auth model class.

        :return: None

        """

        self.cls = models.Auth
        self.data = {
            "school_id": 1,
            "api_token": "foo",
            "push_tokens": [],
            "push_enabled": False,
            "user": models.User(
                id=1
            )
        }


class TestActivityModel(TestJSONModel):
    """
    Test Activity Model Class

    Test class for validating the activity model class.

    Attributes:


    """

    def setUp(self) -> None:
        """
        Set up the data to test with for the activity model class.

        :return: None

        """

        self.cls = models.Activity
        self.data = {
            "id": 1,
            "author_id": 1,
            "classroom_id": 1,
            "normalized_text": "Hello, World!",
            "html": "<h1>Hello, World!</h1>",
            "date": datetime.today().date(),
            "staff_unprocessed": True,
            "photo_url": "https://www.hello.world/photo",
            "medium_photo_url": "https://www.hello.world/medium-photo",
            "large_photo_url": "https://www.hello.world/large-photo",
            "original_photo_url": "https://www.hello.world/original-photo",
            "created_at": datetime.now()
        }


class TestChildModel(TestJSONModel):
    """
    Test Child Model Class

    Test class for validating the child model class.

    Attributes:


    """

    def setUp(self) -> None:
        """
        Set up the data to test with for the child model class.

        :return: None

        """

        self.cls = models.Child
        self.data = {
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


class TestClassroomModel(TestJSONModel):
    """
    Test Classroom Model Class

    Test class for validating the classroom model class.

    Attributes:


    """

    def setUp(self) -> None:
        """
        Set up the data to test with for the classroom model class.

        :return: None

        """

        self.cls = models.Classroom
        self.data = {
            "id": 1,
            "name": "Hello",
            "lesson_set_id": 1,
            "level": "1st Grade",
            "active": True
        }


class TestConferenceReportModel(TestJSONModel):
    """
    Test Conference Report Model Class

    Test class for validating the conference report model class.

    Attributes:


    """

    def setUp(self) -> None:
        """
        Set up the data to test with for the conference report model class.

        :return: None

        """

        self.cls = models.ConferenceReport
        self.data = {
            "id": 1,
            "name": "Hello",
            "child_id": 1,
            "widgets": [{

            }]
        }


class TestEventModel(TestJSONModel):
    """
    Test Event Model Class

    Test class for validating the event model class.

    Attributes:


    """

    def setUp(self) -> None:
        """
        Set up the data to test with for the event model class.

        :return: None

        """

        self.cls = models.Event
        self.data = {
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


class TestFormModel(TestJSONModel):
    """
    Test Form Model Class

    Test class for validating the form model class.

    Attributes:


    """

    def setUp(self) -> None:
        """
        Set up the data to test with for the form model class.

        :return: None

        """

        self.cls = models.Form
        self.data = {
            "id": 1,
            "form_template_id": 1,
            "state": "submitted",
            "child_id": 1,
            "created_at": datetime.now(),
            "fields": {
                "student_first_name": "Hello",
                "student_last_name": "World",
                "parent_name": "Hello, World!",
                "classroom": "Archipelago",
                "release": "yes, yes, yes",
                "signature": "Hello World"
            }
        }


class TestFormTemplateModel(TestJSONModel):
    """
    Test Form Template Model Class

    Test class for validating the form template model class.

    Attributes:


    """

    def setUp(self) -> None:
        """
        Set up the data to test with for the form template model class.

        :return: None

        """

        self.cls = models.FormTemplate
        self.data = {
            "id": 1,
            "name": "Hello, World!",
            "widgets": []
        }


class TestLessonSetModel(TestJSONModel):
    """
    Test Lesson Set Model Class

    Test class for validating the lesson set model class.

    Attributes:


    """

    def setUp(self) -> None:
        """
        Set up the data to test with for the lesson set model class.

        :return: None

        """

        self.cls = models.LessonSet
        self.data = {
            "id": 1,
            "name": "Hello, World!",
            "type": "Group",
            "scales": [],
            "areas": []
        }


class TestLevelModel(TestJSONModel):
    """
    Test Level Model Class

    Test class for validating the level model class.

    Attributes:


    """

    def setUp(self) -> None:
        """
        Set up the data to test with for the level model class.

        :return: None

        """

        self.cls = models.Level
        self.data = {
            "child_id": 1,
            "lesson_id": 1,
            "proficiency": 3,
            "date": datetime.today().date(),
            "planned": True
        }


class TestOnlineApplicationModel(TestJSONModel):
    """
    Test Online Application Model Class

    Test class for validating the online application model class.

    Attributes:


    """

    def setUp(self) -> None:
        """
        Set up the data to test with for the online application model class.

        :return: None

        """

        self.cls = models.OnlineApplication
        self.data = {
            "id": 1,
            "first_name": "John",
            "last_name": "Doe",
            "state": "accepted",
            "created_at": "2016-02-16T09:53:44.684-08:00"
        }


class TestSchoolModel(TestJSONModel):
    """
    Test School Model Class

    Test class for validating the school model class.

    Attributes:


    """

    def setUp(self) -> None:
        """
        Set up the data to test with for the school model class.

        :return: None

        """

        self.cls = models.School
        self.data = {
            "id": 1,
            "name": "Hello, World!",
            "phone": "(XXX) XXX-XXXX",
            "address": "123 Hello World Lane",
            "type": "network",
            "timezone": "Pacific Time (US & Canada)"
        }


class TestSessionModel(TestJSONModel):
    """
    Test Session Model Class

    Test class for validating the session model class.

    Attributes:


    """

    def setUp(self) -> None:
        """
        Set up the data to test with for the session model class.

        :return: None

        """

        self.cls = models.Session
        self.data = {
            "id": 1,
            "name": "Hello World",
            "start_date": datetime.today().date(),
            "stop_date": datetime.today().date(),
            "children": 100,
            "current": True,
            "inactive": False
        }


class TestUserModel(TestJSONModel):
    """
    Test User Model Class

    Test class for validating the user model class.

    Attributes:


    """

    def setUp(self) -> None:
        """
        Set up the data to test with for the user model class.

        :return: None

        """

        self.cls = models.User
        self.data = {
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


if __name__ == '__main__':
    unittest.main()
