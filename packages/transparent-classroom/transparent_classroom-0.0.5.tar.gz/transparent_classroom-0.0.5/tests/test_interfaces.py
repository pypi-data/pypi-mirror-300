import unittest
from transparent_classroom.api.interfaces import fields
from transparent_classroom.api.interfaces import Interface
from transparent_classroom.api.enums import HTTPMethod, EndpointBehavior
from transparent_classroom.api.interfaces.fields.exceptions import InterfaceValidationError


class TestInterface(unittest.TestCase):
    """
    Test Interface Class

    Test class for validating the expected behavior of the API interface model.

    Attributes:


    """

    def setUp(self) -> None:
        """
        Set up the data to test with for the API interface.

        :return: None

        """

        self.interface = Interface(
            method=HTTPMethod.GET,
            behavior=EndpointBehavior.LIST,
            headers=[
                fields.InterfaceField(
                    base=fields.StringField(
                        name="X-TransparentClassroomToken",
                        is_required=True
                    )
                )
            ],
            parameters=[
                fields.InterfaceField(
                    base=fields.ModelIdField(
                        name="child_id"
                    )
                ),
                fields.InterfaceField(
                    base=fields.ModelIdField(
                        name="classroom_id"
                    )
                )
            ]
        )

    def test_adding_header(self) -> None:
        """
        Test adding a single header to the interface.

        :return: None

        """

        self.assertEqual(1, len(self.interface.headers()))
        header = fields.InterfaceField(
            base=fields.ModelIdField(
                name="X-TransparentClassroomMasqueradeId"
            )
        )
        self.interface.add_headers(headers=header)
        self.assertEqual(2, len(self.interface.headers()))
        self.assertIn(header, self.interface.headers())

        # Try adding a duplicate record, should be ignored
        self.interface.add_headers(headers=header)
        self.assertEqual(2, len(self.interface.headers()))

    def test_adding_headers_list(self) -> None:
        """
        Test adding a list of headers to the interface.

        :return: None

        """

        self.assertEqual(1, len(self.interface.headers()))
        headers = [
            fields.InterfaceField(
                base=fields.ModelIdField(
                    name="X-TransparentClassroomMasqueradeId"
                )
            ),
            fields.InterfaceField(
                base=fields.ModelIdField(
                    name="X-TransparentClassroomSchoolId"
                )
            ),
            # Duplicate field that will be ignored for the add
            fields.InterfaceField(
                base=fields.ModelIdField(
                    name="X-TransparentClassroomMasqueradeId"
                )
            )
        ]
        self.interface.add_headers(headers=headers)
        self.assertEqual(3, len(self.interface.headers()))
        self.assertIn(headers[0], self.interface.headers())
        self.assertIn(headers[1], self.interface.headers())

    def test_adding_headers_set(self) -> None:
        """
        Test adding a field set of headers to the interface.

        :return: None

        """

        self.assertEqual(1, len(self.interface.headers()))
        headers = [
            fields.InterfaceField(
                base=fields.ModelIdField(
                    name="X-TransparentClassroomMasqueradeId"
                )
            ),
            fields.InterfaceField(
                base=fields.ModelIdField(
                    name="X-TransparentClassroomSchoolId"
                )
            ),
            # Duplicate field that will be ignored for the add
            fields.InterfaceField(
                base=fields.ModelIdField(
                    name="X-TransparentClassroomSchoolId"
                )
            )
        ]
        header_set = fields.InterfaceFieldSet(fields=headers)
        self.interface.add_headers(headers=header_set)
        self.assertEqual(3, len(self.interface.headers()))
        self.assertIn(headers[0], self.interface.headers())
        self.assertIn(headers[1], self.interface.headers())

    def test_removing_header(self) -> None:
        """
        Test removing a single header from the interface.

        :return: None

        """

        self.assertEqual(1, len(self.interface.headers()))
        header = fields.InterfaceField(
            base=fields.ModelIdField(
                name="X-TransparentClassroomToken"
            )
        )
        self.interface.remove_headers(headers=header)
        self.assertEqual(0, len(self.interface.headers()))
        self.assertNotIn(header, self.interface.headers())

        # Try removing a record when none available.
        self.interface.remove_headers(headers=header)
        self.assertNotIn(header, self.interface.headers())
        self.assertEqual(0, len(self.interface.headers()))

    def test_removing_headers_list(self) -> None:
        """
        Test removing a list of headers from the interface.

        :return: None

        """

        self.assertEqual(1, len(self.interface.headers()))
        headers = [
            fields.InterfaceField(
                base=fields.ModelIdField(
                    name="X-TransparentClassroomToken"
                )
            ),
            fields.InterfaceField(
                base=fields.ModelIdField(
                    name="X-TransparentClassroomMasqueradeId"
                )
            )
        ]
        self.interface.remove_headers(headers=headers)
        self.assertEqual(0, len(self.interface.headers()))
        self.assertNotIn(headers[0], self.interface.headers())
        self.assertNotIn(headers[1], self.interface.headers())

    def test_removing_headers_set(self) -> None:
        """
        Test removing a field set of headers from the interface.

        :return: None

        """

        self.assertEqual(1, len(self.interface.headers()))
        headers = [
            fields.InterfaceField(
                base=fields.ModelIdField(
                    name="X-TransparentClassroomToken"
                )
            ),
            fields.InterfaceField(
                base=fields.ModelIdField(
                    name="X-TransparentClassroomMasqueradeId"
                )
            )
        ]
        header_set = fields.InterfaceFieldSet(fields=headers)
        self.interface.remove_headers(headers=header_set)
        self.assertEqual(0, len(self.interface.headers()))
        self.assertNotIn(headers[0], self.interface.headers())
        self.assertNotIn(headers[1], self.interface.headers())

    def test_adding_parameter(self) -> None:
        """
        Test adding a single parameter to the interface.

        :return: None

        """

        self.assertEqual(2, len(self.interface.parameters()))
        parameter = fields.InterfaceField(
            base=fields.BooleanField(
                name="only_photos"
            )
        )
        self.interface.add_parameters(parameters=parameter)
        self.assertEqual(3, len(self.interface.parameters()))
        self.assertIn(parameter, self.interface.parameters())

        # Try adding a duplicate record, should be ignored
        self.interface.add_parameters(parameters=parameter)
        self.assertEqual(3, len(self.interface.parameters()))

    def test_adding_parameter_list(self) -> None:
        """
        Test adding a list of parameters to the interface.

        :return: None

        """

        self.assertEqual(2, len(self.interface.parameters()))
        parameters = [
            fields.InterfaceField(
                base=fields.BooleanField(
                    name="only_photos"
                )
            ),
            fields.InterfaceField(
                base=fields.BooleanField(
                    name="only_portfolio"
                )
            ),
            # Duplicate field that will be ignored for the add
            fields.InterfaceField(
                base=fields.BooleanField(
                    name="only_photos"
                )
            )
        ]
        self.interface.add_parameters(parameters=parameters)
        self.assertEqual(4, len(self.interface.parameters()))
        self.assertIn(parameters[0], self.interface.parameters())
        self.assertIn(parameters[1], self.interface.parameters())

    def test_adding_parameter_set(self) -> None:
        """
        Test adding a field set of parameters to the interface.

        :return: None

        """

        self.assertEqual(2, len(self.interface.parameters()))
        parameters = [
            fields.InterfaceField(
                base=fields.BooleanField(
                    name="only_photos"
                )
            ),
            fields.InterfaceField(
                base=fields.BooleanField(
                    name="only_portfolio"
                )
            ),
            # Duplicate field that will be ignored for the add
            fields.InterfaceField(
                base=fields.BooleanField(
                    name="only_photos"
                )
            )
        ]
        parameter_set = fields.InterfaceFieldSet(fields=parameters)
        self.interface.add_parameters(parameters=parameter_set)
        self.assertEqual(4, len(self.interface.parameters()))
        self.assertIn(parameters[0], self.interface.parameters())
        self.assertIn(parameters[1], self.interface.parameters())

    def test_removing_parameter(self) -> None:
        """
        Test removing a single parameter to the interface.

        :return: None

        """

        self.assertEqual(2, len(self.interface.parameters()))
        parameter = fields.InterfaceField(
            base=fields.BooleanField(
                name="child_id"
            )
        )
        self.interface.remove_parameters(parameters=parameter)
        self.assertEqual(1, len(self.interface.parameters()))
        self.assertNotIn(parameter, self.interface.parameters())

        # Try removing a record that has already been removed, should be ignored
        self.interface.remove_parameters(parameters=parameter)
        self.assertEqual(1, len(self.interface.parameters()))

    def test_removing_parameter_list(self) -> None:
        """
        Test removing a list of parameters from the interface.

        :return: None

        """

        self.assertEqual(2, len(self.interface.parameters()))
        parameters = [
            fields.InterfaceField(
                base=fields.BooleanField(
                    name="child_id"
                )
            ),
            fields.InterfaceField(
                base=fields.ModelIdField(
                    name="classroom_id"
                )
            )
        ]
        self.interface.remove_parameters(parameters=parameters)
        self.assertEqual(0, len(self.interface.parameters()))
        self.assertNotIn(parameters[0], self.interface.parameters())
        self.assertNotIn(parameters[1], self.interface.parameters())

        # Try removing records that have already been removed, should be ignored
        self.interface.remove_parameters(parameters=parameters)
        self.assertEqual(0, len(self.interface.parameters()))

    def test_removing_parameter_set(self) -> None:
        """
        Test removing a field set of parameters from the interface.

        :return: None

        """

        self.assertEqual(2, len(self.interface.parameters()))
        parameters = [
            fields.InterfaceField(
                base=fields.BooleanField(
                    name="child_id"
                )
            ),
            fields.InterfaceField(
                base=fields.ModelIdField(
                    name="classroom_id"
                )
            )
        ]
        parameter_set = fields.InterfaceFieldSet(fields=parameters)
        self.interface.remove_parameters(parameters=parameter_set)
        self.assertEqual(0, len(self.interface.parameters()))
        self.assertNotIn(parameters[0], self.interface.parameters())
        self.assertNotIn(parameters[1], self.interface.parameters())

        # Try removing records that have already been removed, should be ignored
        self.interface.remove_parameters(parameters=parameters)
        self.assertEqual(0, len(self.interface.parameters()))

    def test_properties(self) -> None:
        """
        Test the properties of the interface object.

        :return: None

        """

        self.assertEqual(HTTPMethod.GET, self.interface.method)
        self.assertEqual(EndpointBehavior.LIST, self.interface.behavior)

        # Set new values and check them
        self.interface.method = HTTPMethod.POST
        self.interface.behavior = EndpointBehavior.SHOW
        self.assertEqual(HTTPMethod.POST, self.interface.method)
        self.assertEqual(EndpointBehavior.SHOW, self.interface.behavior)

    def test_validation(self) -> None:
        """
        Test running validation on a provided set of headers and parameters.

        :return: None

        """

        configs = {
            "headers": {
                "X-TransparentClassroomToken": "1"
            },
            "parameters": {
                "child_id": 1,
                "classroom_id": 1
            }
        }
        self.assertEqual(configs, self.interface.validate(**configs))
        configs["headers"]["X-TransparentClassroomToken"] = 1
        self.assertRaises(InterfaceValidationError, self.interface.validate, **configs)


if __name__ == '__main__':
    unittest.main()
