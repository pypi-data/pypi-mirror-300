import unittest
from transparent_classroom.api.interfaces.validators import Validator, constraints, exceptions


class TestValidator(unittest.TestCase):
    """
    Test Validators Class

    Test class for checking the functionality of the validator object.

    Attributes:


    """

    def setUp(self) -> None:
        """
        Set up the validators to test with.

        :return: None

        """

        self.validator1 = Validator(
            constraints=[
                constraints.IsGreaterThan(min_value=10)
            ]
        )
        self.validator2 = Validator(
            constraints=[
                constraints.IsGreaterThan(min_value=10),
                constraints.IsPositiveInteger()
            ]
        )
        self.validator3 = Validator(
            constraints=[
                constraints.IsString()
            ]
        )
        self.validator4 = Validator(
            constraints=[
                constraints.IsGreaterThan(min_value=10),
                constraints.IsPositiveInteger()
            ]
        )

    def test_comparator(self) -> None:
        """
        Test the comparator operator of the validator.

        :return: None

        """

        # Non-required constraints
        self.assertNotEqual(self.validator1, self.validator2)
        self.assertNotEqual(self.validator1, self.validator3)
        self.assertEqual(self.validator2, self.validator4)
        self.assertNotEqual(self.validator3, self.validator4)
        self.assertNotEqual(self.validator1, Validator())

        # Non-required constraints
        self.validator2.is_required = True
        self.assertTrue(self.validator2.is_required)
        self.assertNotEqual(self.validator2, self.validator4)
        self.validator4.add(constraints=[constraints.IsRequired()])
        self.assertEqual(self.validator2, self.validator4)

    def test_containment(self) -> None:
        """
        Test the containment (`in`) method on the validator object.

        :return: None

        """

        self.assertTrue(constraints.IsGreaterThan(min_value=10) in self.validator1)
        self.assertTrue(constraints.IsGreaterThan(min_value=5) not in self.validator1)
        self.assertTrue(constraints.IsPositiveInteger() in self.validator2)
        self.assertTrue(constraints.IsInteger() not in self.validator2)
        self.assertTrue(constraints.IsString() in self.validator3)
        self.assertTrue(constraints.IsRequired() not in self.validator1)
        self.validator1.is_required = True
        self.assertTrue(constraints.IsRequired() in self.validator1)

    def test_length(self) -> None:
        """
        Test the length method of the validator (which returns the number of
        constraints in the validator).

        :return: None

        """

        self.assertEqual(len(self.validator1), 1)
        self.assertEqual(len(self.validator2), 2)
        self.assertEqual(len(self.validator3), 1)

        self.validator1.is_required = True
        self.assertTrue(self.validator1.is_required)
        self.assertTrue(len(self.validator1), 2)
        self.validator1.is_required = False
        self.assertFalse(self.validator1.is_required)
        self.assertTrue(len(self.validator1), 1)

    def test_add(self) -> None:
        """
        Test the validator method for adding a new constraint.

        :return: None

        """

        self.assertEqual(len(self.validator1), 1)
        self.assertTrue(constraints.IsInteger() not in self.validator1)
        self.assertTrue(self.validator1.is_valid(11.5))
        self.assertFalse(self.validator1.is_valid(9))

        self.validator1.add(constraints=constraints.IsInteger())
        self.assertEqual(len(self.validator1), 2)
        self.assertTrue(constraints.IsInteger() in self.validator1)
        self.assertTrue(self.validator1.is_valid(12))
        self.assertFalse(self.validator1.is_valid(11.5))
        self.assertFalse(self.validator1.is_valid(9))

    def test_clear(self) -> None:
        """
        Test the validator method for clearing all constraints.

        :return: None

        """

        self.assertEqual(len(self.validator1), 1)

        # Test clearing the constraints
        self.validator1.clear()
        self.assertEqual(len(self.validator1), 0)

        # Test adding constraints back in and validating with them
        self.validator1.add(constraints=[constraints.IsNumeric(), constraints.IsGreaterThan()])
        self.assertEqual(len(self.validator1), 2)
        self.assertTrue(self.validator1.is_valid(1))
        self.assertFalse(self.validator1.is_valid(-1))

        # Test requiring a valid
        self.validator1.is_required = True
        self.assertEqual(len(self.validator1), 3)
        self.assertFalse(self.validator1.is_valid(None))

        # Check that required parameter is removed and set to False
        self.validator1.clear()
        self.assertEqual(len(self.validator1), 0)
        self.assertFalse(self.validator1.is_required)

    def test_remove(self) -> None:
        """
        Test the validator method for removing a constraint.

        :return: None

        """

        # Test validator with IsGreaterThan constraint
        self.assertTrue(self.validator1.is_valid(value=15))
        self.assertTrue(self.validator1.is_valid(value=None))
        self.assertFalse(self.validator1.is_valid(value=-5))
        self.assertFalse(self.validator1.is_valid(value="Hello"))
        self.validator1.remove(constraints=constraints.IsGreaterThan(min_value=10))
        self.assertTrue(self.validator1.is_valid(value=15))
        self.assertTrue(self.validator1.is_valid(value=-5))
        self.assertTrue(self.validator1.is_valid(value="Hello"))
        self.assertTrue(self.validator1.is_valid(value=None))

        # Test validator with str constraint
        self.assertTrue(self.validator3.is_valid(value="Test"))
        self.assertTrue(self.validator3.is_valid(value=None))
        self.assertFalse(self.validator3.is_valid(value=-5))
        self.assertFalse(self.validator3.is_valid(value=0))
        self.validator3.is_required = True
        self.assertTrue(len(self.validator3), 2)
        self.validator3.remove(constraints=[constraints.IsRequired()])
        self.assertTrue(len(self.validator3), 1)
        self.assertFalse(self.validator3.is_required)

    def test_is_valid(self) -> None:
        """
        Test the validator `is_valid` method.

        :return: None

        """

        # Test non-strict validation
        self.assertTrue(self.validator1.is_valid(value=11))
        self.assertTrue(self.validator1.is_valid(value=None))
        self.assertFalse(self.validator1.is_valid(value=10))
        self.assertFalse(self.validator1.is_valid(value=True))
        self.assertFalse(self.validator1.is_valid(value="hello"))
        self.assertTrue(self.validator1.is_valid(value=13.3))
        self.assertTrue(self.validator2.is_valid(value=11))
        self.assertFalse(self.validator2.is_valid(value=13.3))
        self.assertTrue(self.validator3.is_valid(value="Hello"))
        self.assertFalse(self.validator3.is_valid(value=False))

        # Test strict validation
        self.validator1.is_required = True
        self.assertTrue(self.validator1.is_valid(value=20, strict=True))
        self.assertTrue(self.validator1.is_valid(value=25.5, strict=True))
        self.assertRaises(exceptions.NumericValueError, self.validator1.is_valid, **{"value": "No", "strict": True})
        self.assertRaises(exceptions.NullFieldException, self.validator1.is_valid, **{"value": None, "strict": True})


if __name__ == '__main__':
    unittest.main()
