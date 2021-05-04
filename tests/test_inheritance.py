from .test_base import TestBase
from tests.example_models.child_model import ChildModel, ParentModel
from src.openapi_annotations import api_models, get_spec
import tests.example_controllers.event_routes


class InheritanceTests(TestBase):
    def test_model_annotation(self):
        self.assertIsNotNone(self.get_model(ParentModel))
        self.assertIsNotNone(self.get_model(ChildModel))

    def test_model_base_class(self):
        child_model = self.get_model(ChildModel)

        self.assertEqual(child_model['bases'][0]
                         ['module'], ParentModel.__module__)
        self.assertEqual(child_model['bases'][0]['name'], ParentModel.__name__)

    def test_parent_properties_are_in_model(self):
        spec = get_spec('openapi')
        child_model = spec['components']['schemas'][ChildModel.__name__]

        self.assertTrue('base_property' in child_model['properties'])
