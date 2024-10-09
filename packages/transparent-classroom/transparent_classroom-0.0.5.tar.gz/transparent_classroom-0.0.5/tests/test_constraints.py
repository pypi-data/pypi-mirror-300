import numbers
import unittest
from datetime import date, datetime
from transparent_classroom.api.interfaces.validators import constraints
from transparent_classroom.api.interfaces.validators import exceptions


class TestConstraint(unittest.TestCase):
    """
    Test Constraint Class

    Test class for testing the base object methods of constraints (comparators, etc.).

    Attributes:


    """

    def test_base(self) -> None:
        """
        Test the comparator to make sure that the

        :return: None

        """

        constraint_types = [
            constraints.IsNumeric, constraints.IsInteger, constraints.IsDate, constraints.IsList,
            constraints.IsDateTime, constraints.IsBoolean, constraints.IsPositiveInteger, constraints.IsString,
            constraints.IsGreaterThan
        ]

        for i in range(0, len(constraint_types)):
            for j in range(i, len(constraint_types)):
                c1, c2 = constraint_types[i](), constraint_types[j]()

                for b1 in [True, False]:
                    for b2 in [True, False]:
                        c1.nullable, c2.nullable = b1, b2

                        if (i == j) and (b1 == b2):
                            self.assertEqual(c1, c2)
                            self.assertEqual(hash(c1), hash(c2))
                        else:
                            self.assertNotEqual(c1, c2)
                            self.assertNotEqual(hash(c1), hash(c2))


class TestTypeConstraint(unittest.TestCase):
    """
    Test IsType Constraint Class

    Test class for testing the is-type constraint.

    Attributes:


    """

    def test_base_constraint(self) -> None:
        """
        Test the base IsType constraint class.

        :return: None

        """

        constraint = constraints.IsType(data_type=object, exception_type=ValueError)

        # Handling None (nullable)
        self.assertTrue(constraint.nullable)
        self.assertTrue(constraint.is_valid(value=None, strict=False))
        self.assertTrue(constraint.is_valid(value=None, strict=True))

        # Handling None (non-nullable)
        constraint.nullable = False
        self.assertFalse(constraint.nullable)
        self.assertFalse(constraint.is_valid(value=None, strict=False))
        self.assertRaises(exceptions.NullFieldException, constraint.is_valid, **{"value": None, "strict": True})

    def test_numeric_constraint(self) -> None:
        """
        Test the numeric constraint class.

        :return: None

        """

        constraint = constraints.IsNumeric(nullable=True)

        # Check parameters
        self.assertEqual(constraint.data_type, numbers.Number)
        self.assertEqual(constraint.exception_type, exceptions.NumericValueError)

        # Non-strict Validity Checks
        self.assertTrue(constraint.is_valid(value=1, strict=False))
        self.assertTrue(constraint.is_valid(value=5.2, strict=False))
        self.assertTrue(constraint.is_valid(value=-1.2, strict=False))
        self.assertFalse(constraint.is_valid(value="-1.2", strict=False))
        self.assertFalse(constraint.is_valid(value="Hello", strict=False))
        self.assertFalse(constraint.is_valid(value=True, strict=False))

        # Strict Validity Checks
        self.assertTrue(constraint.is_valid(value=1, strict=True))
        self.assertTrue(constraint.is_valid(value=5.2, strict=True))
        self.assertTrue(constraint.is_valid(value=-1.2, strict=True))
        self.assertRaises(exceptions.NumericValueError, constraint.is_valid, **{"value": "-1.2", "strict": True})
        self.assertRaises(exceptions.NumericValueError, constraint.is_valid, **{"value": False, "strict": True})

    def test_integer_constraint(self) -> None:
        """
        Test the integer constraint class.

        :return: None

        """

        constraint = constraints.IsInteger(nullable=True)

        # Check parameters
        self.assertEqual(constraint.data_type, int)
        self.assertEqual(constraint.exception_type, exceptions.IntegerValueError)

        # Non-strict Validity Checks
        self.assertTrue(constraint.is_valid(value=1, strict=False))
        self.assertTrue(constraint.is_valid(value=0, strict=False))
        self.assertTrue(constraint.is_valid(value=-3, strict=False))
        self.assertFalse(constraint.is_valid(value="Hello", strict=False))
        self.assertFalse(constraint.is_valid(value="1.2", strict=False))
        self.assertFalse(constraint.is_valid(value=-1.2, strict=False))
        self.assertFalse(constraint.is_valid(value=5.7, strict=False))
        self.assertFalse(constraint.is_valid(value=[], strict=False))
        self.assertFalse(constraint.is_valid(value=True, strict=False))

        # Strict Validity Checks
        self.assertTrue(constraint.is_valid(value=1, strict=True))
        self.assertTrue(constraint.is_valid(value=0, strict=True))
        self.assertTrue(constraint.is_valid(value=-1, strict=True))
        self.assertRaises(exceptions.IntegerValueError, constraint.is_valid, **{"value": "Hello", "strict": True})
        self.assertRaises(exceptions.IntegerValueError, constraint.is_valid, **{"value": "1.2", "strict": True})
        self.assertRaises(exceptions.IntegerValueError, constraint.is_valid, **{"value": 5.7, "strict": True})
        self.assertRaises(exceptions.IntegerValueError, constraint.is_valid, **{"value": [], "strict": True})
        self.assertRaises(exceptions.IntegerValueError, constraint.is_valid, **{"value": False, "strict": True})

    def test_positive_integer_constraint(self) -> None:
        """
        Test the positive integer constraint class.

        :return: None

        """

        constraint = constraints.IsPositiveInteger(nullable=True)

        # Check parameters
        self.assertEqual(constraint.data_type, int)
        self.assertEqual(constraint.exception_type, exceptions.IntegerValueError)

        # Non-strict Validity Checks
        self.assertTrue(constraint.is_valid(value=1, strict=False))
        self.assertTrue(constraint.is_valid(value=5, strict=False))
        self.assertFalse(constraint.is_valid(value="1", strict=False))
        self.assertFalse(constraint.is_valid(value=-1, strict=False))
        self.assertFalse(constraint.is_valid(value=1.2, strict=False))
        self.assertFalse(constraint.is_valid(value=0, strict=False))
        self.assertFalse(constraint.is_valid(value={}, strict=False))
        self.assertFalse(constraint.is_valid(value=True, strict=False))

        # Strict Validity Checks
        self.assertTrue(constraint.is_valid(value=1, strict=True))
        self.assertTrue(constraint.is_valid(value=5, strict=True))
        self.assertRaises(exceptions.IntegerValueError, constraint.is_valid, **{"value": "1", "strict": True})
        self.assertRaises(exceptions.NotGreaterThanValueError, constraint.is_valid, **{"value": -1, "strict": True})
        self.assertRaises(exceptions.IntegerValueError, constraint.is_valid, **{"value": 1.2, "strict": True})
        self.assertRaises(exceptions.NotGreaterThanValueError, constraint.is_valid, **{"value": 0, "strict": True})
        self.assertRaises(exceptions.IntegerValueError, constraint.is_valid, **{"value": False, "strict": True})
        self.assertRaises(exceptions.IntegerValueError, constraint.is_valid, **{"value": {}, "strict": True})

    def test_string_constraint(self) -> None:
        """
        Test the string constraint class.

        :return: None

        """

        constraint = constraints.IsString(nullable=True)

        # Check parameters
        self.assertEqual(constraint.data_type, str)
        self.assertEqual(constraint.exception_type, exceptions.StringValueError)

        # Non-strict Validity Checks
        self.assertTrue(constraint.is_valid(value="Hello", strict=False))
        self.assertTrue(constraint.is_valid(value="", strict=False))
        self.assertTrue(constraint.is_valid(value="1", strict=False))
        self.assertFalse(constraint.is_valid(value=1, strict=False))
        self.assertFalse(constraint.is_valid(value=1.2, strict=False))
        self.assertFalse(constraint.is_valid(value=[], strict=False))
        self.assertFalse(constraint.is_valid(value=True, strict=False))

        # Strict Validity Checks
        self.assertTrue(constraint.is_valid(value="Hello", strict=True))
        self.assertTrue(constraint.is_valid(value="0", strict=True))
        self.assertRaises(exceptions.StringValueError, constraint.is_valid, **{"value": 1, "strict": True})
        self.assertRaises(exceptions.StringValueError, constraint.is_valid, **{"value": 1.2, "strict": True})
        self.assertRaises(exceptions.StringValueError, constraint.is_valid, **{"value": [], "strict": True})
        self.assertRaises(exceptions.StringValueError, constraint.is_valid, **{"value": False, "strict": True})

    def test_boolean_constraint(self) -> None:
        """
        Test the boolean constraint class.

        :return: None

        """

        constraint = constraints.IsBoolean(nullable=True)

        # Non-strict Validity Checks
        self.assertTrue(constraint.is_valid(value="true", strict=False))
        self.assertTrue(constraint.is_valid(value="false", strict=False))
        self.assertFalse(constraint.is_valid(value="1", strict=False))
        self.assertFalse(constraint.is_valid(value=1, strict=False))
        self.assertFalse(constraint.is_valid(value=1.2, strict=False))
        self.assertFalse(constraint.is_valid(value=[], strict=False))

        # Strict Validity Checks
        self.assertTrue(constraint.is_valid(value="true", strict=True))
        self.assertTrue(constraint.is_valid(value="false", strict=True))

    def test_list_constraint(self) -> None:
        """
        Test the list constraint class.

        :return: None

        """

        constraint = constraints.IsList(nullable=True)

        # Check parameters
        self.assertEqual(constraint.data_type, list)
        self.assertEqual(constraint.exception_type, exceptions.ListValueError)

        # Non-strict Validity Checks
        self.assertTrue(constraint.is_valid(value=[], strict=False))
        self.assertTrue(constraint.is_valid(value=[1, 2, 3], strict=False))
        self.assertFalse(constraint.is_valid(value="1", strict=False))
        self.assertFalse(constraint.is_valid(value=1, strict=False))
        self.assertFalse(constraint.is_valid(value=1.2, strict=False))
        self.assertFalse(constraint.is_valid(value={}, strict=False))
        self.assertFalse(constraint.is_valid(value=True, strict=False))

        # Strict Validity Checks
        self.assertTrue(constraint.is_valid(value=["Hello", "World"], strict=True))
        self.assertRaises(exceptions.ListValueError, constraint.is_valid, **{"value": "1", "strict": True})
        self.assertRaises(exceptions.ListValueError, constraint.is_valid, **{"value": 1, "strict": True})
        self.assertRaises(exceptions.ListValueError, constraint.is_valid, **{"value": 1.2, "strict": True})
        self.assertRaises(exceptions.ListValueError, constraint.is_valid, **{"value": False, "strict": True})
        self.assertRaises(exceptions.ListValueError, constraint.is_valid, **{"value": {}, "strict": True})

    def test_date_constraint(self) -> None:
        """
        Test the date constraint class.

        :return: None

        """

        constraint = constraints.IsDate(nullable=True)

        # Check parameters
        self.assertEqual(constraint.data_type, date)
        self.assertEqual(constraint.exception_type, exceptions.DateValueError)

        # Non-strict Validity Checks
        self.assertTrue(constraint.is_valid(value=datetime.today().date(), strict=False))
        self.assertFalse(constraint.is_valid(value=datetime.today(), strict=False))
        self.assertFalse(constraint.is_valid(value=[1, 2, 3], strict=False))
        self.assertFalse(constraint.is_valid(value="1", strict=False))
        self.assertFalse(constraint.is_valid(value=1, strict=False))
        self.assertFalse(constraint.is_valid(value=1.2, strict=False))
        self.assertFalse(constraint.is_valid(value={}, strict=False))
        self.assertFalse(constraint.is_valid(value=True, strict=False))

        # Strict Validity Checks
        self.assertTrue(constraint.is_valid(value=datetime.today().date(), strict=True))
        self.assertRaises(exceptions.DateValueError, constraint.is_valid, **{"value": datetime.today(), "strict": True})
        self.assertRaises(exceptions.DateValueError, constraint.is_valid, **{"value": "1", "strict": True})
        self.assertRaises(exceptions.DateValueError, constraint.is_valid, **{"value": 1, "strict": True})
        self.assertRaises(exceptions.DateValueError, constraint.is_valid, **{"value": 1.2, "strict": True})
        self.assertRaises(exceptions.DateValueError, constraint.is_valid, **{"value": False, "strict": True})
        self.assertRaises(exceptions.DateValueError, constraint.is_valid, **{"value": {}, "strict": True})

    def test_datetime_constraint(self) -> None:
        """
        Test the datetime constraint class.

        :return: None

        """

        constraint = constraints.IsDateTime(nullable=True)

        # Check parameters
        self.assertEqual(constraint.data_type, datetime)
        self.assertEqual(constraint.exception_type, exceptions.DateTimeValueError)

        # Non-strict Validity Checks
        self.assertTrue(constraint.is_valid(value=datetime.today(), strict=False))
        self.assertFalse(constraint.is_valid(value=datetime.today().date(), strict=False))
        self.assertFalse(constraint.is_valid(value=[1, 2, 3], strict=False))
        self.assertFalse(constraint.is_valid(value="1", strict=False))
        self.assertFalse(constraint.is_valid(value=1, strict=False))
        self.assertFalse(constraint.is_valid(value=1.2, strict=False))
        self.assertFalse(constraint.is_valid(value={}, strict=False))
        self.assertFalse(constraint.is_valid(value=True, strict=False))

        # Strict Validity Checks
        self.assertTrue(constraint.is_valid(value=datetime.today(), strict=True))
        self.assertRaises(exceptions.DateTimeValueError, constraint.is_valid, **{"value": datetime.today().date(), "strict": True})
        self.assertRaises(exceptions.DateTimeValueError, constraint.is_valid, **{"value": "1", "strict": True})
        self.assertRaises(exceptions.DateTimeValueError, constraint.is_valid, **{"value": 1, "strict": True})
        self.assertRaises(exceptions.DateTimeValueError, constraint.is_valid, **{"value": 1.2, "strict": True})
        self.assertRaises(exceptions.DateTimeValueError, constraint.is_valid, **{"value": False, "strict": True})
        self.assertRaises(exceptions.DateTimeValueError, constraint.is_valid, **{"value": {}, "strict": True})


class TestSelectionConstraint(unittest.TestCase):
    """
    Test Selection Constraint Class

    Test class for testing the selection constraint that limits available options to
    a finite list of known elements.

    Attributes:


    """

    def test_hash(self) -> None:
        """
        Test the selection constraint's hash method.

        :return: None

        """

        c1 = constraints.SelectionConstraint(options=['hello', 'world'])
        c2 = constraints.SelectionConstraint(options=['hello', 'goodbye', 'now', 'world'])
        c3 = constraints.SelectionConstraint(options=[])
        c4 = constraints.SelectionConstraint(options=['hello', 'world'])
        c5 = constraints.SelectionConstraint(options=['hello', 'world', 'world'])

        # Check nullable
        self.assertEqual(hash(c1), hash(c4))
        self.assertEqual(hash(c1), hash(c5))
        self.assertNotEqual(hash(c1), hash(c2))
        self.assertNotEqual(hash(c2), hash(c3))

        # Check nullable
        c1.nullable = False
        c2.nullable = False
        self.assertNotEqual(hash(c1), hash(c4))
        self.assertNotEqual(hash(c1), hash(c2))

    def test_comparator(self) -> None:
        """
        Test the selection constraint's equality method.

        :return: None

        """

        c1 = constraints.SelectionConstraint(options=["hello", "world"])
        c2 = constraints.SelectionConstraint(options=["hello", "goodbye", "now", "world"])
        c3 = constraints.SelectionConstraint(options=[])
        c4 = constraints.SelectionConstraint(options=["hello", "world"])
        c5 = constraints.SelectionConstraint(options=["hello", "world", "world"])

        # Check nullable
        self.assertEqual(c1, c4)
        self.assertEqual(c1, c5)
        self.assertNotEqual(c1, c2)
        self.assertNotEqual(c2, c3)

        # Check nullable
        c1.nullable = False
        c2.nullable = False
        self.assertNotEqual(c1, c4)
        self.assertNotEqual(c1, c2)

    def test_single_value_select(self) -> None:
        """
        Test the selection constraint's validation method (with a single value selected).

        :return: None

        """

        constraint = constraints.SelectionConstraint(options=["hello", 0, True, 3.3])

        # Non-strict Validity Checks
        self.assertTrue(constraint.nullable)
        self.assertTrue(constraint.is_valid(value="hello"))
        self.assertTrue(constraint.is_valid(value=0))
        self.assertTrue(constraint.is_valid(value=True))
        self.assertTrue(constraint.is_valid(value=3.3))
        self.assertFalse(constraint.is_valid(value="world"))
        self.assertFalse(constraint.is_valid(value=1))
        self.assertFalse(constraint.is_valid(value=False))
        self.assertFalse(constraint.is_valid(value=3.2))

        # Strict Validity Checks
        self.assertTrue(constraint.is_valid(value="hello"))
        self.assertTrue(constraint.is_valid(value=0))
        self.assertTrue(constraint.is_valid(value=True))
        self.assertTrue(constraint.is_valid(value=3.3))
        self.assertRaises(exceptions.SelectionValueError, constraint.is_valid, **{"value": "world", "strict": True})
        self.assertRaises(exceptions.SelectionValueError, constraint.is_valid, **{"value": 1, "strict": True})
        self.assertRaises(exceptions.SelectionValueError, constraint.is_valid, **{"value": False, "strict": True})
        self.assertRaises(exceptions.SelectionValueError, constraint.is_valid, **{"value": 3.2, "strict": True})

        # Handling None (non-nullable)
        constraint.nullable = False
        self.assertFalse(constraint.nullable)
        self.assertFalse(constraint.is_valid(value=None, strict=False))
        self.assertRaises(exceptions.NullFieldException, constraint.is_valid, **{"value": None, "strict": True})

    def test_multi_value_select(self) -> None:
        """
        Test the selection constraint's validation method (with multiple values selected).

        :return: None

        """

        constraint = constraints.SelectionConstraint(options=["hello", 0, True, 3.3])

        # Non-strict validity checks
        self.assertTrue(constraint.is_valid(value=[0, 3.3, "hello"]))
        self.assertTrue(constraint.is_valid(value=[True, 0, 3.3, "hello"]))
        self.assertFalse(constraint.is_valid(value=[True, 0, 3.3, "world"]))
        self.assertFalse(constraint.is_valid(value=[False, 1, 3.3, "world"]))


class TestIsRequiredConstraint(unittest.TestCase):
    """
    Test Is Required Constraint Class

    Test class for testing the is required constraint.

    Attributes:


    """

    def test_validation(self) -> None:
        """
        Test the is required constraint's validation method.

        :return: None

        """

        constraint = constraints.IsRequired()

        # Non-strict Validity Checks
        self.assertTrue(constraint.is_valid(value="hello"))
        self.assertTrue(constraint.is_valid(value=0))
        self.assertFalse(constraint.is_valid(value=None))

        # Strict Validity Checks
        self.assertTrue(constraint.is_valid(value="hello", strict=True))
        self.assertTrue(constraint.is_valid(value=0, strict=True))
        self.assertRaises(exceptions.NullFieldException, constraint.is_valid, **{"value": None, "strict": True})


class TestIsGreaterThanConstraint(unittest.TestCase):
    """
    Test Is Greater Than Constraint Class

    Attributes:


    """

    def test_hash(self) -> None:
        """
        Test the inequality constraint's hash method.

        :return: None

        """

        c1 = constraints.IsGreaterThan()
        c2 = constraints.IsGreaterThan(min_value=-6)
        c3 = constraints.IsGreaterThan(min_value=4)
        c4 = constraints.IsGreaterThan(min_value=-6)

        # Check nullable
        self.assertEqual(hash(c2), hash(c4))
        self.assertNotEqual(hash(c1), hash(c2))
        self.assertNotEqual(hash(c1), hash(c3))
        self.assertNotEqual(hash(c2), hash(c3))

        # Check nullable
        c1.nullable = False
        c2.nullable = False
        self.assertNotEqual(hash(c1), hash(c2))
        self.assertNotEqual(hash(c2), hash(c4))

    def test_validation(self) -> None:
        """
        Test the inequality constraint's validation.

        :return: None

        """

        c1 = constraints.IsGreaterThan()
        c2 = constraints.IsGreaterThan(min_value=-6)
        c3 = constraints.IsGreaterThan(min_value=4)
        c4 = constraints.IsGreaterThan(min_value=-6)

        # Non-strict Validity Checks
        self.assertTrue(c1.is_valid(value=1))
        self.assertTrue(c2.is_valid(value=100))
        self.assertTrue(c3.is_valid(value=40))
        self.assertTrue(c4.is_valid(value=0))
        self.assertFalse(c1.is_valid(value=-1))
        self.assertFalse(c1.is_valid(value="hello"))
        self.assertFalse(c1.is_valid(value=[]))
        self.assertFalse(c1.is_valid(value=True))
        self.assertFalse(c2.is_valid(value=-6))

        # Strict Validity Checks
        c1.nullable = False
        self.assertTrue(c1.is_valid(value=1, strict=True))
        self.assertTrue(c2.is_valid(value=100, strict=True))
        self.assertRaises(exceptions.NullFieldException, c1.is_valid, **{"value": None, "strict": True})
        self.assertRaises(exceptions.NumericValueError, c1.is_valid, **{"value": "Hello", "strict": True})
        self.assertRaises(exceptions.NotGreaterThanValueError, c1.is_valid, **{"value": 0, "strict": True})


if __name__ == '__main__':
    unittest.main()
