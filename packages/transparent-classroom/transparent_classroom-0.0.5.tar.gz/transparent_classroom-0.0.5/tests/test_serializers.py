import operator
import unittest
from datetime import date, datetime
from functools import reduce
from transparent_classroom.models import Child, OnlineApplication, Model
from transparent_classroom.models import serializers, deserializers


class TestSerializer(unittest.TestCase):
    """
    Test Serializer Class

    Test class for testing the expected behavior of the serializer object(s).

    Attributes:


    """

    """
    The model to test serialization against.
    
    """
    model = Model(id=1)

    """
    The serializer to test.

    """
    serializer = serializers.Serializer(mapping={"id": "id"})

    @staticmethod
    def __get_from_dict(data_dict, map_list):
        try:
            return reduce(operator.getitem, map_list, data_dict)
        except Exception:
            return None

    def test_serialize(self) -> None:
        """
        Test serializing the provided object into a JSON/data dict.

        :return: None

        """

        data = self.serializer.serialize(obj=self.model)
        model_json = self.model.to_json()

        for attr, path in self.serializer.mapping.items():
            path = path if isinstance(path, list) else [path]
            expected = model_json[attr]
            actual = self.__get_from_dict(data_dict=data, map_list=path)
            self.assertEqual(expected, actual)

    def test_serialize_batch(self) -> None:
        """
        Test serializing a list of models into JSON records /data dicts

        :return: None

        """

        objs = [self.model]
        objs_data = self.serializer.batch(objs=objs)

        for i in range(0, len(objs)):
            model_json = objs[i].to_json()

            for attr, path in self.serializer.mapping.items():
                path = path if isinstance(path, list) else [path]
                expected = model_json[attr]
                actual = self.__get_from_dict(data_dict=objs_data[i], map_list=path)
                self.assertEqual(expected, actual)


class TestChildSerializer(TestSerializer):
    """
    Test Child Serializer Class

    Test class for testing the expected behavior of the child serializer object.

    Attributes:


    """

    def setUp(self) -> None:
        """
        Set up the data to test the child serializer with.

        :return: None

        """

        self.model = Child(
            id=1,
            first_name="Hello",
            last_name="World",
            birth_date=date.today(),
            gender="F",
            profile_photo="https://www.helloworld.com/profile-picture.jpg",
            program="Elementary",
            ethnicity=["Caucasian"],
            household_income="middle",
            dominant_language="English",
            grade="2nd",
            student_id="1",
            hours_string="8:00AM(8:15AM) - 3:00PM M-F",
            allergies=None,
            notes="Hello World",
            first_day=date.today(),
            last_day=None,
            exit_notes=None,
            exit_reason=None,
            exit_survey_id=None,
            parent_ids=[1, 2],
            classroom_ids=[1, 2]
        )
        self.serializer = serializers.ChildSerializer()


class TestOnlineApplicationSerializer(TestSerializer):
    """
    Test Online Application Serializer Class

    Test class for testing the expected behavior of the online application serializer object.

    Attributes:


    """

    def setUp(self) -> None:
        """
        Set up the data to test the online application serializer with.

        :return: None

        """

        self.model = OnlineApplication(
            id=1,
            first_name="John",
            last_name="Doe",
            state="accepted",
            created_at=datetime.today()
        )
        self.serializer = serializers.OnlineApplicationSerializer()


if __name__ == '__main__':
    unittest.main()
