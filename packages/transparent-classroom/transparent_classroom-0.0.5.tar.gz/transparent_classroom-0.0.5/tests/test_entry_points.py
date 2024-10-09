import unittest
from transparent_classroom.api.enums import ModelType
from transparent_classroom.api.entry_points import EntryPoint
from transparent_classroom.api.interfaces import fields, Interface
from transparent_classroom.api.enums import HTTPMethod, EndpointBehavior
from transparent_classroom.api.routing.routes import RouteComponent, Route


class TestEntryPoint(unittest.TestCase):
    """
    Test Entry Point Class

    Test class for validating the expected behavior of the entry point model.

    Attributes:


    """

    def setUp(self) -> None:
        """
        Set up the data to test with for the API interface.

        :return: None

        """

        self.route = Route(
            model_type=ModelType.CHILDREN,
            components=[
                RouteComponent(sub_path="api/v1"),
                RouteComponent(sub_path="{{ model_name }}")
            ]
        )
        self.interface = Interface(
            method=HTTPMethod.GET,
            behavior=EndpointBehavior.LIST,
            headers=[
                fields.InterfaceField(base=fields.StringField(name="X-TransparentClassroomToken", is_required=True)),
                fields.InterfaceField(base=fields.ModelIdField(name="X-TransparentClassroomMasqueradeId")),
                fields.InterfaceField(base=fields.ModelIdField(name="X-TransparentClassroomSchoolId"))
            ],
            parameters=[
               fields.InterfaceField(base=fields.ModelIdField(name="classroom_id")),
               fields.InterfaceField(base=fields.ModelIdField(name="session_id")),
               fields.InterfaceField(base=fields.BooleanField(name="only_current")),
               fields.InterfaceField(base=fields.PositiveIntegerField(name="page")),
               fields.InterfaceField(base=fields.PositiveIntegerField(name="per_page"))
            ]
        )
        self.entry_point = EntryPoint(
            name="Test Entry Point",
            route=self.route,
            interface=self.interface
        )

    def test_properties(self) -> None:
        """
        Test the properties of the entry point.

        :return: None

        """

        self.assertEqual("Test Entry Point", self.entry_point.name)
        self.assertEqual(self.route.model_type, self.entry_point.model_type)
        self.assertEqual(self.route, self.entry_point.route)
        self.assertEqual(self.interface, self.entry_point.interface)


if __name__ == '__main__':
    unittest.main()

