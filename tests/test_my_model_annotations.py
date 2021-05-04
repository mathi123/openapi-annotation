from .test_base import TestBase
from tests.example_models.my_model import MyModel
from src.openapi_annotations import api_models


class MyModelTests(TestBase):
    def test_model_annotation(self):
        self.assertIsNotNone(self.get_model(MyModel))

    def test_model_description_from_docstring(self):
        self.assertEqual(self.get_model(MyModel)[
                         'description'], 'The first model from this API.')

    def test_property_uuid_format(self):
        result = self.get_model(MyModel)
        id_property = list(filter(lambda x: x['name'] == 'id', result['attributes']))[0]
        self.assertEqual(id_property['data_format'], 'uuid')

    def test_property_docstring_ends_up_in_description(self):
        result = self.get_model(MyModel)
        documented_property = list(filter(lambda x: x['name'] == 'documented_property', result['attributes']))[0]
        self.assertEqual(documented_property['description'], 'Property documentation.')
