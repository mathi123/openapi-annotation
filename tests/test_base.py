from unittest import TestCase
from src.openapi_annotations import api_models


class TestBase(TestCase):
    def get_model(self, model_type):
        models = list(
            filter(lambda x: x['name'] == model_type.__name__, api_models))
        return None if len(models) == 0 else models[0]