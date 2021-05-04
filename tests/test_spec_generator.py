import tests.example_controllers.event_routes
import json
import os
from src.openapi_annotations import get_spec
from http import HTTPStatus
from .test_base import TestBase
from openapi_spec_validator import validate_spec
from openapi_spec_validator.readers import read_from_filename


class SpecGeneratorTests(TestBase):
    def test_open_api_tag(self):
        spec = get_spec('test api', camel_case=True, default_response_descriptions={
            HTTPStatus.INTERNAL_SERVER_ERROR: 'Unexpected internal server error.',
            HTTPStatus.NO_CONTENT: 'Operation succeeded. Nothing to return.',
            HTTPStatus.NOT_FOUND: 'Could not find data.',
            HTTPStatus.CREATED: 'Resource was created successfully.',
            HTTPStatus.BAD_REQUEST: 'Invalid input data.',
            HTTPStatus.OK: 'Success.'
        }, default_parameter_descriptions={
            'skip': 'The number of data records to skip before fetching a page.',
            'take': 'Number of records to return. Use value -1 to get all data.',
            'sortColumn': 'The database field to sort by. Use python_syntax for the field name.',
            'sortDirection': 'The direction to sort by (asc or desc).',
            'createdAt': 'Filter on the creation date. Use an exact date, or a date range e.g. \'[2018-01-01,2019-01-01[\', \']2018-01-01,\' or \'2015-01-01\'',
            'modifiedAt': 'Filter on the last modification date. Use an exact date, or a date range e.g. \'[2018-01-01,2019-01-01[\', \']2018-01-01,\' or \'2015-01-01\'',
            'ids': 'Ids to match.'
        })
        self.assertEqual(spec['openapi'], '3.0.0')
        os.makedirs('./temp', exist_ok=True)
        spec_file = './temp/openapi.json'
        with open(spec_file, 'w') as file:
            file.write(json.dumps(spec, indent=4))
            spec_dict, spec_url = read_from_filename(spec_file)
            validate_spec(spec_dict)