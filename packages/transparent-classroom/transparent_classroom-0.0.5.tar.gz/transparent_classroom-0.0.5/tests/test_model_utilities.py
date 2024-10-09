import pytz
import unittest
from datetime import datetime, date
from transparent_classroom.models.utilities import Formatter


class TestFormatter(unittest.TestCase):
    """
    Test Formatter Class

    Test class for validating the expected behavior of model (JSON) formatter.

    Attributes:


    """

    def setUp(self) -> None:
        """
        Set up the data to test the formatter with.

        :return: None

        """

        self.formatter = Formatter()

    def test_to_json(self) -> None:
        """
        Test the dict conversion to a JSON-safe string/dict.

        :return: None

        """

        d, dt = date.today(), datetime.now(pytz.utc)
        ds, dts = date.strftime(d, "%Y-%m-%d"), datetime.strftime(dt, "%Y-%m-%dT%H:%M:%S.%f%z")
        data = {
            "property_1": "Hello, World!",
            "property_2": d,
            "property_3": dt,
            "property_4": {
                "property_1": "Hello, World!",
                "property_2": d,
                "property_3": dt,
                "property_4": {
                    "property_1": d
                }
            },
            "property_5": [
                "Hello, World!",
                d,
                dt,
                {
                    "property_1": "Hello, World!",
                    "property_2": d,
                    "property_3": dt,
                    "property_4": {
                        "property_1": d
                    }
                }
            ]
        }
        expected_json_data = {
            "property_1": "Hello, World!",
            "property_2": ds,
            "property_3": dts,
            "property_4": {
                "property_1": "Hello, World!",
                "property_2": ds,
                "property_3": dts,
                "property_4": {
                    "property_1": ds
                }
            },
            "property_5": [
                "Hello, World!",
                ds,
                dts,
                {
                    "property_1": "Hello, World!",
                    "property_2": ds,
                    "property_3": dts,
                    "property_4": {
                        "property_1": ds
                    }
                }
            ]
        }
        json_data = self.formatter.jsonify(data=data)
        self.assertEqual(expected_json_data, json_data)

    def test_date_to_str(self) -> None:
        """
        Test the conversion of a date object to a string (in the expected format
        of Transparent Classroom).

        :return: None

        """

        d = datetime.today().date()
        ds = date.strftime(d, "%Y-%m-%d")
        self.assertEqual(ds, self.formatter.date_to_str(value=d))
        self.assertEqual(ds, self.formatter.date_to_str(value=ds))
        self.assertRaises(ValueError, self.formatter.date_to_str, {"value": "Hello, World."})

    def test_datetime_to_str(self) -> None:
        """
        Test the conversion of a datetime object to a string (in the expected format
        of Transparent Classroom).

        :return: None

        """

        dt = datetime.now(pytz.utc)
        dts = datetime.strftime(dt, "%Y-%m-%dT%H:%M:%S.%f%z")
        self.assertEqual(dts, self.formatter.datetime_to_str(value=dt))
        self.assertEqual(dts, self.formatter.datetime_to_str(value=dts))
        self.assertRaises(ValueError, self.formatter.datetime_to_str, {"value": "Hello, World."})

    def test_str_to_date(self) -> None:
        """
        Test the conversion of a string to a date object (in the expected format
        of Transparent Classroom).

        :return: None

        """

        d = datetime.today().date()
        ds = date.strftime(d, "%Y-%m-%d")
        self.assertEqual(d, self.formatter.str_to_date(value=ds))
        self.assertEqual(d, self.formatter.str_to_date(value=d))
        self.assertRaises(ValueError, self.formatter.str_to_date, {"value": "Hello, World."})

    def test_str_to_datetime(self) -> None:
        """
        Test the conversion of a string to a datetime object (in the expected format
        of Transparent Classroom).

        :return: None

        """

        dt = datetime.now(pytz.utc)
        dts = datetime.strftime(dt, "%Y-%m-%dT%H:%M:%S.%f%z")
        self.assertEqual(dt, self.formatter.str_to_datetime(value=dts))
        self.assertEqual(dt, self.formatter.str_to_datetime(value=dt))
        self.assertRaises(ValueError, self.formatter.str_to_datetime, {"value": "Hello, World."})


if __name__ == '__main__':
    unittest.main()
