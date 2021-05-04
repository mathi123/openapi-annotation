from .test_base import TestBase
import tests.example_controllers.event_routes
from src.openapi_annotations import api_routes, api_models


class RoutesTests(TestBase):
    def test_model_annotation(self):
        self.assertEqual(len(api_routes), 5)
