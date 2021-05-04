from .test_base import TestBase
from tests.example_models.event import Event
from tests.example_models.change_tracking_model import ChangeTrackingModel
from tests.example_models.id_name_model import IdNameModel
from src.openapi_annotations import get_spec


class MultiInheritanceTests(TestBase):
    def test_model_annotation(self):
        self.assertIsNotNone(self.get_model(Event))
        self.assertIsNotNone(self.get_model(ChangeTrackingModel))
        self.assertIsNotNone(self.get_model(IdNameModel))

    def test_model_base_class(self):
        child_model = self.get_model(Event)

        self.assertEqual(len(child_model['bases']), 2)

    def test_parent_properties_are_in_model(self):
        spec = get_spec('openapi')
        child_model = spec['components']['schemas'][Event.__name__]

        self.assertTrue('created_at' in child_model['properties'])
