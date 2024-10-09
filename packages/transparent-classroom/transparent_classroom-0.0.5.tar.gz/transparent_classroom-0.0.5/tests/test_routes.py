import unittest
from transparent_classroom.api.enums import ModelType
from transparent_classroom.api.routing.routes import RouteComponent, Route


class TestRoute(unittest.TestCase):
    """
    Test Routes Class

    Test class for validating the expected behavior of route objects.

    Attributes:


    """

    def setUp(self) -> None:
        """
        Set up the routes to test with.

        :return: None

        """

        # Get user route
        self.route1 = Route(
            model_type=ModelType.USERS,
            components=[
                RouteComponent(sub_path="api/v1"),
                RouteComponent(sub_path="{{ model_name }}"),
                RouteComponent(sub_path="{{ object_id }}")
            ]
        )

        # List users route
        self.route2 = Route(
            model_type=ModelType.USERS,
            components=[
                RouteComponent(sub_path="api/v1"),
                RouteComponent(sub_path="{{ model_name }}")
            ]
        )

        # Get child route
        self.route3 = Route(
            model_type=ModelType.CHILDREN,
            components=[
                RouteComponent(sub_path="api/v1"),
                RouteComponent(sub_path="{{ model_name }}"),
                RouteComponent(sub_path="{{ object_id }}")
            ]
        )

    def test_comparator(self) -> None:
        """
        Test the class/object comparator.

        :return: None

        """

        self.assertNotEqual(self.route1, self.route2)
        self.assertNotEqual(self.route1, self.route3)
        self.assertNotEqual(self.route2, self.route3)

        self.route3.model_type = ModelType.USERS
        self.assertEqual(self.route1, self.route3)

    def test_add_component(self) -> None:
        """
        Test adding components to the route.

        :return: None

        """

        self.route2.add(components=RouteComponent(sub_path="{{ object_id }}"))
        self.assertEqual(self.route1, self.route2)

        path = self.route2.path.replace(self.route2.suffix, "")
        route_component_sub_paths = ["test1", "test2", "test3"]

        for route_component_sub_path in route_component_sub_paths:
            self.route2.add(components=RouteComponent(sub_path=route_component_sub_path))

        expected_path = "/".join([path] + route_component_sub_paths) + self.route2.suffix
        self.assertEqual(expected_path, self.route2.path)

    def test_remove_component(self) -> None:
        """
        Test removing components from the route.

        :return: None

        """

        self.route1.remove(components=RouteComponent(sub_path="{{ object_id }}"))
        self.assertEqual(self.route1, self.route2)

    def test_apply(self) -> None:
        """
        Test applying variables to the route for path construction.

        :return: None

        """

        model_name = ModelType.USERS.value
        object_id = 1
        expected_path = f"api/v1/{model_name}/{object_id}.json"
        path = self.route1.apply(**{"model_name": model_name, "object_id": object_id})
        self.assertEqual(expected_path, path)


if __name__ == '__main__':
    unittest.main()
