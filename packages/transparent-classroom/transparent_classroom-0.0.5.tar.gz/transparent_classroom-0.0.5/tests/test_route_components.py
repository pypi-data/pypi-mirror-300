import copy
import unittest
from transparent_classroom.api.routing.routes import RouteComponent


class TestRouteComponent(unittest.TestCase):
    """
    Test Route Components Class

    Test class for validating the expected behavior of route components.

    Attributes:


    """

    def test_subpath(self) -> None:
        """
        Test the subpath setter.

        :return: None

        """

        sub_path = "/api/test/path/"
        route_component = RouteComponent(sub_path=sub_path)
        self.assertNotEqual(sub_path, route_component.sub_path)
        self.assertEqual(sub_path.strip("/"), route_component.sub_path)

    def test_comparator(self) -> None:
        """
        Test the class/object comparator.

        :return: None

        """

        route_component_1 = RouteComponent(sub_path="hello")
        route_component_2 = RouteComponent(sub_path="world")
        route_component_3 = RouteComponent(sub_path="hello")
        self.assertEqual(route_component_1, route_component_3)
        self.assertNotEqual(route_component_1, route_component_2)

    def test_copy(self) -> None:
        """
        Test copying the object.

        :return: None

        """

        route_component = RouteComponent(sub_path="hello")
        route_component_copy = copy.copy(route_component)
        self.assertEqual(route_component, route_component_copy)


if __name__ == '__main__':
    unittest.main()
