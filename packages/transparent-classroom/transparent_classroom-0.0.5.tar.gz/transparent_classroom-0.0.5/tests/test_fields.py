import unittest
from typing import List
from datetime import datetime
from transparent_classroom.api.interfaces import fields
from transparent_classroom.api.interfaces.validators import Validator
from transparent_classroom.api.interfaces.validators import constraints, exceptions
from transparent_classroom.api.interfaces.fields.exceptions import InterfaceValidationError


class TestAttribute(unittest.TestCase):
    """
    Test Attributes Class

    Test class for validating the named API attributes object.

    Attributes:


    """

    def setUp(self) -> None:
        """
        Set up the named attributes to test with.

        :return: None

        """

        self.attribute1 = fields.NamedAPIAttribute(name="Hello")
        self.attribute2 = fields.NamedAPIAttribute(name="World")
        self.attribute3 = fields.NamedAPIAttribute(name="Hello")

    def test_comparator(self) -> None:
        """
        Test the class/object comparator.

        :return: None

        """

        self.assertNotEqual(self.attribute1, self.attribute2)
        self.assertEqual(self.attribute1, self.attribute3)

    def test_hash(self) -> None:
        """
        Test the class/object hashing.

        :return: None

        """

        self.assertNotEqual(hash(self.attribute1), hash(self.attribute2))
        self.assertEqual(hash(self.attribute1), hash(self.attribute3))

    def test_repr(self) -> None:
        """
        Test the str/repr conversions methods.

        :return: None

        """

        self.assertEqual(str(self.attribute1), "Attribute `Hello`")
        self.assertEqual(str(self.attribute2), "Attribute `World`")
        self.assertEqual(str(self.attribute1), str(self.attribute3))
        self.assertEqual(repr(self.attribute1), "Attribute `Hello`")
        self.assertEqual(repr(self.attribute2), "Attribute `World`")
        self.assertEqual(repr(self.attribute1), repr(self.attribute3))

    def test_properties(self) -> None:
        """
        Test the get/set methods for the class properties.

        :return: None

        """

        self.assertEqual(self.attribute1.name, "Hello")
        self.assertEqual(self.attribute2.name, "World")
        self.assertEqual(self.attribute3.name, "Hello")

        self.attribute1.name = "Goodbye"
        self.assertEqual(self.attribute1.name, "Goodbye")
        self.assertNotEqual(self.attribute1.name, self.attribute3.name)


class TestField(unittest.TestCase):
    """
    Test Fields Class

    Test class for validating the base Field class.

    Attributes:


    """

    def setUp(self) -> None:
        """
        Set up the fields to test with.

        :return: None

        """

        self.field1 = fields.Field(
            name="id",
            value=1,
            validator=Validator(
                constraints=[
                    constraints.IsPositiveInteger()
                ]
            )
        )
        self.field2 = fields.Field(
            name="first_name",
            value="Hello",
            validator=Validator(
                constraints=[
                    constraints.IsString()
                ]
            )
        )
        self.field3 = fields.Field(
            name="last_name",
            value="World",
            validator=Validator(
                constraints=[
                    constraints.IsString()
                ]
            )
        )

    def test_comparator(self) -> None:
        """
        Test the class/object comparator.

        :return: None

        """

        self.assertNotEqual(self.field1, self.field2)
        self.assertNotEqual(self.field1, self.field3)
        self.assertNotEqual(self.field2, self.field3)

        tmp = fields.Field(
            name=self.field1.name,
            value=self.field1.value,
            validator=Validator(
                constraints=[
                    constraints.IsPositiveInteger()
                ]
            )
        )
        self.assertFalse(tmp.is_required)
        self.assertEqual(self.field1, tmp)
        tmp.is_required = True
        self.assertNotEqual(self.field1, tmp)

    def test_hash(self) -> None:
        """
        Test the class/object hashing.

        :return: None

        """

        self.assertNotEqual(hash(self.field1), hash(self.field2))
        self.assertNotEqual(hash(self.field1), hash(self.field3))
        self.assertNotEqual(hash(self.field2), hash(self.field3))

        # hashing is based off name + value
        tmp = fields.Field(name=self.field1.name, value=self.field1.value)
        self.assertEqual(hash(self.field1), hash(tmp))

    def test_repr(self) -> None:
        """
        Test the str/repr conversions methods.

        :return: None

        """

        self.assertEqual(str(self.field1), "Field `id` = 1")
        self.assertEqual(str(self.field2), "Field `first_name` = Hello")
        self.assertEqual(str(self.field3), "Field `last_name` = World")
        self.assertEqual(repr(self.field1), "Field `id` = 1")
        self.assertEqual(repr(self.field2), "Field `first_name` = Hello")
        self.assertEqual(repr(self.field3), "Field `last_name` = World")

    def test_validation(self) -> None:
        """
        Test the field's validation.

        :return: None

        """

        # Test validity of setup values
        self.assertTrue(self.field1.is_valid())
        self.assertTrue(self.field2.is_valid())
        self.assertTrue(self.field3.is_valid())
        self.assertTrue(self.field1.is_valid(strict=True))
        self.assertTrue(self.field2.is_valid(strict=True))
        self.assertTrue(self.field3.is_valid(strict=True))

        # Test validity of invalid values
        self.field1.value = "Hello, World"
        self.field2.value = -1
        self.field3.value = ["Hello", "World"]
        self.assertFalse(self.field1.is_valid())
        self.assertFalse(self.field2.is_valid())
        self.assertFalse(self.field3.is_valid())

        # Test strict validity of invalid values
        self.assertRaises(exceptions.IntegerValueError, self.field1.is_valid, **{"strict": True})
        self.assertRaises(exceptions.StringValueError, self.field2.is_valid, **{"strict": True})
        self.assertRaises(exceptions.StringValueError, self.field3.is_valid, **{"strict": True})

        self.field1.value = None
        self.field1.is_required = True
        self.assertFalse(self.field1.is_valid())
        self.assertRaises(exceptions.NullFieldException, self.field1.is_valid, **{"strict": True})


class TestSpecializedField(unittest.TestCase):
    """
    Test Specialized Fields Class

    Test class for validating the specialized fields.

    Attributes:


    """

    def _test_entries(self, field: fields.Field, values: List, expected: bool) -> None:
        """
        Test the entries and compare them to the expected value.

        :param field: fields.Field, The field to run validation against.
        :param values: List, The values to test on the field.
        :param expected: bool, The expected `is_valid` response.
        :return: None

        """

        for value in values:
            field.value = value
            self.assertEqual(field.is_valid(), expected)

    def _test_valid_entries(self, field: fields.Field, values: List) -> None:
        """
        Test the provided entries that are expected to be valid.

        :param field: fields.Field, The field to run validation against.
        :param values: List, The (expected to be valid) values to test on the field.
        :return: None

        """

        self._test_entries(field=field, values=values, expected=True)

    def _test_invalid_entries(self, field: fields.Field, values: List) -> None:
        """
        Test the provided entries that are expected to be invalid.

        :param field: fields.Field, The field to run validation against.
        :param values: List, The (expected to be invalid) values to test on the field.
        :return: None

        """

        self._test_entries(field=field, values=values, expected=False)

    def test_positive_integer_field(self) -> None:
        """
        Test the positive integer field.

        :return: None

        """

        valid_values = [1, None]
        invalid_values = [0, -5, 3.3, None, "Hello, World", [], {}, datetime.today().date(), datetime.now()]
        field = fields.PositiveIntegerField(name="test_positive_integer")
        self._test_valid_entries(field=field, values=valid_values)
        field.is_required = True
        self._test_invalid_entries(field=field, values=invalid_values)

    def test_model_id_field(self) -> None:
        """
        Test the model id field.

        :return: None

        """

        valid_values = [1, None]
        invalid_values = [0, -5, 3.3, None, "Hello, World", [], {}, datetime.today().date(), datetime.now(), True]
        field = fields.ModelIdField(name="test_model_id")
        self._test_valid_entries(field=field, values=valid_values)
        field.is_required = True
        self._test_invalid_entries(field=field, values=invalid_values)

    def test_string_field(self) -> None:
        """
        Test the string field.

        :return: None

        """

        valid_values = ["Hello, World", None, ""]
        invalid_values = [0, -5, 3.3, None, 500, [], {}, datetime.today().date(), datetime.now(), True]
        field = fields.StringField(name="test_string")
        self._test_valid_entries(field=field, values=valid_values)
        field.is_required = True
        self._test_invalid_entries(field=field, values=invalid_values)

    def test_boolean_field(self) -> None:
        """
        Test the boolean field.

        :return: None

        """

        valid_values = ["true", "false", None]
        invalid_values = [1, 0, -5, 3.3, None, 500, [], {}, datetime.today().date(), datetime.now()]
        field = fields.BooleanField(name="test_bool")
        self._test_valid_entries(field=field, values=valid_values)
        field.is_required = True
        self._test_invalid_entries(field=field, values=invalid_values)

    def test_date_field(self) -> None:
        """
        Test the date field.

        :return: None

        """

        valid_values = [datetime.today().date(), None]
        invalid_values = [1, 0, -5, 3.3, None, 500, [], {}, True, datetime.now()]
        field = fields.DateField(name="test_date")
        self._test_valid_entries(field=field, values=valid_values)
        field.is_required = True
        self._test_invalid_entries(field=field, values=invalid_values)

    def test_datetime_field(self) -> None:
        """
        Test the datetime field.

        :return: None

        """

        valid_values = [datetime.now(), datetime.today(), None]
        invalid_values = [1, 0, -5, 3.3, None, 500, [], {}, True, datetime.today().date()]
        field = fields.DateTimeField(name="test_datetime")
        self._test_valid_entries(field=field, values=valid_values)
        field.is_required = True
        self._test_invalid_entries(field=field, values=invalid_values)

    def test_select_field(self) -> None:
        """
        Test the select field.

        :return: None

        """

        options = ["Hello", "World", 1, True]
        valid_values = ["Hello", 1, True]
        invalid_values = [0, -5, 3.3, None, 500, [], {}, False, datetime.today().date()]
        field = fields.SelectField(name="test_select", options=options)
        self._test_valid_entries(field=field, values=valid_values)
        field.is_required = True
        self._test_invalid_entries(field=field, values=invalid_values)

    def test_multi_select_field(self) -> None:
        """
        Test the multi select field.

        :return: None

        """

        options = ["Hello", "World", 1, True, 3.25, datetime.today().date()]
        valid_values = [["Hello"], [1, True], [datetime.today().date(), 3.25, 1]]
        invalid_values = [[0, -5], [3.3, None], [500, [], {}], ["Hello", "World", False]]
        field = fields.SelectField(name="test_multi_select", options=options)
        self._test_valid_entries(field=field, values=valid_values)
        field.is_required = True
        self._test_invalid_entries(field=field, values=invalid_values)


class TestInterfaceField(unittest.TestCase):
    """
    Test Interface Fields Class

    Test class for validating interface fields.

    Attributes:


    """

    def setUp(self) -> None:
        """
        Set up the interface fields to test with.

        :return: None

        """

        self.interface_field = fields.InterfaceField(base=fields.ModelIdField(name="model_id"))

    def test_repr(self) -> None:
        """
        Test the str/repr conversions methods.

        :return: None

        """

        field_name = f"Interface Field `{self.interface_field.base.name}_interface_field`"
        self.assertEqual(str(self.interface_field), field_name)
        self.assertEqual(repr(self.interface_field), field_name)

    def test_validation(self) -> None:
        """
        Test validation on the interface field.

        :return: None

        """

        self.assertTrue(self.interface_field.is_valid(value=1))
        self.assertTrue(self.interface_field.is_valid(value=10))
        self.assertTrue(self.interface_field.is_valid(value=None))
        self.assertFalse(self.interface_field.is_valid(value=0))
        self.assertFalse(self.interface_field.is_valid(value=-5))
        self.assertFalse(self.interface_field.is_valid(value="Hello, World"))
        self.assertFalse(self.interface_field.is_valid(value=2.2))

    def test_bind(self) -> None:
        """
        Test the bind method for the interface field.

        :return: None

        """

        field = self.interface_field.bind(value=1)
        self.assertEqual(field.name, self.interface_field.base.name)
        self.assertEqual(field.value, 1)
        self.assertRaises(exceptions.IntegerValueError, self.interface_field.bind, **{"value": 3.3})
        self.assertRaises(exceptions.IntegerValueError, self.interface_field.bind, **{"value": "Hello"})
        self.assertRaises(exceptions.NotGreaterThanValueError, self.interface_field.bind, **{"value": 0})


class TestFieldSet(unittest.TestCase):
    """
    Test Field Sets Class

    Test class for validating the expected behavior of field sets.

    Attributes:


    """

    def setUp(self) -> None:
        """
        Set up the field set to test with.

        :return: None

        """

        self.field_set = fields.FieldSet(
            fields=[
                fields.ModelIdField(name="test_id"),
                fields.StringField(name="test_string"),
                fields.BooleanField(name="test_boolean"),
                fields.DateField(name="test_date")
            ]
        )

    def test_field_accessors(self) -> None:
        """
        Test the field accessor methods.

        :return: None

        """

        # Test on valid keys/field names
        field = self.field_set.get("test_id")
        self.assertEqual(field.name, "test_id")
        field = self.field_set["test_string"]
        self.assertEqual(field.name, "test_string")

        # Test on invalid keys/field names
        self.assertIsNone(self.field_set.get("test_missing"))
        self.assertIsNone(self.field_set["test_missing"])

    def test_add_fields(self) -> None:
        """
        Test adding fields to the field set.

        :return: None

        """

        # Test adding a string field to the field set
        self.assertEqual(len(self.field_set), 4)
        field = fields.StringField(name="first_name")
        self.field_set.add(fields=field)
        self.assertEqual(len(self.field_set), 5)
        self.assertEqual(self.field_set["first_name"], field)

        # Try adding the same field multiple times
        self.field_set.add(fields=[field, field, field])
        self.assertEqual(len(self.field_set), 5)
        self.field_set.add(fields=field)
        self.field_set.add(fields=field)
        self.assertEqual(len(self.field_set), 5)

        # Add two new distinct fields
        self.field_set.add(fields=[fields.StringField(name="last_name"), fields.DateField(name="birth_date")])
        self.assertEqual(len(self.field_set), 7)
        self.assertIsNotNone(self.field_set.get(name="last_name"))
        self.assertIsNotNone(self.field_set["birth_date"])

    def test_clearing_fields(self) -> None:
        """
        Test clearing the fields from the field set.

        :return: None

        """

        self.assertEqual(len(self.field_set), 4)
        self.assertIsNotNone(self.field_set["test_id"])
        self.field_set.clear()
        self.assertEqual(len(self.field_set), 0)
        self.assertIsNone(self.field_set["test_id"])

    def test_removing_fields_with_strings(self) -> None:
        """
        Test removing fields from the field set with strings.

        :return: None

        """

        # Test removal with strings
        self.assertEqual(len(self.field_set), 4)
        self.field_set.remove(fields="test_id")
        self.assertEqual(len(self.field_set), 3)
        self.assertIsNone(self.field_set["test_id"])
        self.field_set.remove(fields=["test_string", "test_boolean"])
        self.assertEqual(len(self.field_set), 1)
        self.assertIsNone(self.field_set["test_string"])
        self.assertIsNone(self.field_set["test_boolean"])

    def test_removing_fields_with_fields(self) -> None:
        """
        Test removing fields from the field set with field objects.

        :return: None

        """

        # Test removal with Field objects
        self.assertEqual(len(self.field_set), 4)
        self.field_set.remove(fields=fields.ModelIdField(name="test_id"))
        self.assertEqual(len(self.field_set), 3)
        self.assertIsNone(self.field_set["test_id"])
        self.field_set.remove(fields=[fields.StringField(name="test_string"), fields.BooleanField(name="test_boolean")])
        self.assertEqual(len(self.field_set), 1)
        self.assertIsNone(self.field_set["test_string"])
        self.assertIsNone(self.field_set["test_boolean"])

    def test_removing_fields_with_mixed_entries(self) -> None:
        """
        Test removing fields from the field set with mixed entries.

        :return: None

        """

        # Test removal with Field objects
        self.assertEqual(len(self.field_set), 4)
        self.field_set.remove(fields=[fields.StringField(name="test_string"), "test_boolean"])
        self.assertEqual(len(self.field_set), 2)
        self.assertIsNone(self.field_set["test_string"])
        self.assertIsNone(self.field_set["test_boolean"])

    def test_removing_fields_with_field_set(self) -> None:
        """
        Test removing fields from the field set with another field set

        :return: None

        """

        # Test removal with Field objects
        self.assertEqual(len(self.field_set), 4)
        removal_field_set = fields.FieldSet(
            fields=[
                fields.ModelIdField(name="test_id"),
                fields.BooleanField(name="test_boolean")
            ]
        )
        self.field_set.remove(fields=removal_field_set)
        self.assertEqual(len(self.field_set), 2)
        self.assertIsNone(self.field_set["test_id"])
        self.assertIsNone(self.field_set["test_boolean"])

    def test_to_json(self) -> None:
        """
        Test converting the field set to a dict/JSON object.

        :return: None

        """

        data_dict = {
            "test_id": 1,
            "test_string": "Hello, World",
            "test_boolean": True,
            "test_date": datetime.now().date()
        }

        for k, v in data_dict.items():
            self.assertIsNotNone(self.field_set[k])
            self.field_set[k].value = v

        for k, v in self.field_set.to_json().items():
            self.assertEqual(v, data_dict[k])

    def test_to_list(self) -> None:
        """
        Test converting the field set to a list

        :return: None

        """

        fields = self.field_set.to_list()
        self.assertEqual(len(fields), len(self.field_set))

        for field in fields:
            self.assertEqual(field, self.field_set.get(name=field.name))


class TestInterfaceFieldSet(unittest.TestCase):
    """
    Test Interface Field Sets Class

    Test class for validating the expected behavior of the interface field set object.

    Attributes:


    """

    def setUp(self) -> None:
        """
        Set up the field set to test with.

        :return: None

        """

        self.field_set = fields.InterfaceFieldSet(
            fields=[
                fields.InterfaceField(base=fields.ModelIdField(name="test_id")),
                fields.InterfaceField(base=fields.StringField(name="test_string")),
                fields.InterfaceField(base=fields.BooleanField(name="test_boolean")),
                fields.InterfaceField(base=fields.DateField(name="test_date"))
            ]
        )

    def test_add_fields(self) -> None:
        """
        Test adding fields to the interface field set.

        :return: None

        """

        # Test adding a string field to the field set
        self.assertEqual(len(self.field_set), 4)
        field = fields.InterfaceField(base=fields.StringField(name="first_name"))
        self.field_set.add(fields=field)
        self.assertEqual(len(self.field_set), 5)
        self.assertEqual(self.field_set["first_name_interface_field"], field)

        # Try adding the same field multiple times
        self.field_set.add(fields=[field, field, field])
        self.assertEqual(len(self.field_set), 5)
        self.field_set.add(fields=field)
        self.field_set.add(fields=field)
        self.assertEqual(len(self.field_set), 5)

        # Add two new distinct fields
        f1 = fields.InterfaceField(base=fields.StringField(name="last_name"))
        f2 = fields.InterfaceField(base=fields.DateField(name="birth_date"))
        self.field_set.add(fields=[f1, f2])
        self.assertEqual(len(self.field_set), 7)
        self.assertIsNotNone(self.field_set.get(name="last_name_interface_field"))
        self.assertIsNotNone(self.field_set["birth_date_interface_field"])

    def test_removing_fields(self) -> None:
        """
        Test removing fields from the interface field set.

        :return: None

        """

        # Test removal with strings
        self.assertEqual(len(self.field_set), 4)
        self.assertIsNotNone(self.field_set["test_id_interface_field"])
        self.field_set.remove(fields="test_id_interface_field")
        self.assertEqual(3, len(self.field_set))
        self.assertIsNone(self.field_set["test_id_interface_field"])

        # Test removal with field
        self.assertIsNotNone(self.field_set["test_string_interface_field"])
        field = fields.InterfaceField(base=fields.StringField(name="test_string"))
        self.field_set.remove(fields=field)
        self.assertEqual(2, len(self.field_set))
        self.assertIsNone(self.field_set["test_string_interface_field"])

    def test_validation(self) -> None:
        """
        Test the bulk validation method of the interface field set.

        :return: None

        """

        valid_bindings = {
            "test_id": 1,
            "test_string": "Hello, World",
            "test_boolean": True,
            "test_date": datetime.today().date()
        }
        invalid_bindings = {
            "test_id": "25",
            "test_string": -4,
            "test_boolean": 1,
            "test_date": datetime.now()
        }
        self.assertTrue(self.field_set.validate(bindings=valid_bindings))
        self.assertRaises(InterfaceValidationError, self.field_set.validate, **{"bindings": invalid_bindings})


if __name__ == '__main__':
    unittest.main()
