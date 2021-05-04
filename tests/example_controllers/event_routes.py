from typing import Dict, List
from tests.example_models.date_filter import DateFilter
from tests.example_models.page import Page
from tests.example_models.event import Event
from src.openapi_annotations import api_response, api_parameter,\
    api_route, Methods, ParameterTypes, Schema, StringFormats
from http import HTTPStatus
import json

endpoint = '/events'
detail_endpoint = f'/events/{{eventId}}'
sort_directions = ['asc', 'desc']


@api_parameter(ParameterTypes.Query, 'skip', int, minimum=0)
@api_parameter(ParameterTypes.Query, 'take', int, minimum=-1)
@api_parameter(ParameterTypes.Query, 'sortColumn', str)
@api_parameter(ParameterTypes.Query, 'sortDirection', str, enum=sort_directions)
@api_parameter(ParameterTypes.Query, 'createdAt', str)
@api_parameter(ParameterTypes.Query, 'modifiedAt', str)
@api_parameter(ParameterTypes.Query, 'startDate', str, description='Date filter on the start date of the event.')
@api_parameter(ParameterTypes.Query, 'endDate', str, description='Date filter on the end date of the event.')
@api_parameter(ParameterTypes.Query, 'ids', schema=Schema(data_type=list, items_schema=Schema(data_type=str, data_format=StringFormats.Uuid)))
@api_parameter(ParameterTypes.Query, 'query', str)
@api_response(HTTPStatus.OK, Page[Event])
@api_response(HTTPStatus.INTERNAL_SERVER_ERROR)
@api_route(Methods.Get, endpoint)
def events_get(skip: int = 0, take: int = 25, sort_column: str = 'description',
               sort_direction: str = 'asc', query: str = None,
               start_date: str = None, end_date: str = None,
               ids: List[str] = None, created_at: str = None, modified_at: str = None):
    """Gets a page of events."""
    result = Page(data=[], total=0)
    # Todo: json serialization
    return json.dumps(result)


@api_response(HTTPStatus.CREATED, Event)
@api_response(HTTPStatus.BAD_REQUEST)
@api_response(HTTPStatus.INTERNAL_SERVER_ERROR)
@api_route(Methods.Post, endpoint, Event)
def events_post(body=None):
    """Creates a new event and returns it."""
    result = {}
    return json.dumps(result), 201


@api_parameter(ParameterTypes.Path, 'eventId', str, data_format=StringFormats.Uuid, description='Id of the event.')
@api_response(HTTPStatus.NO_CONTENT)
@api_response(HTTPStatus.NOT_FOUND)
@api_response(HTTPStatus.INTERNAL_SERVER_ERROR)
@api_route(Methods.Delete, detail_endpoint)
def events_event_id_delete(event_id: str):
    """Deletes an event."""
    return '', 204


@api_parameter(ParameterTypes.Path, 'eventId', str, data_format=StringFormats.Uuid, description='Id of the event.')
@api_response(HTTPStatus.OK, Event)
@api_response(HTTPStatus.NOT_FOUND)
@api_response(HTTPStatus.INTERNAL_SERVER_ERROR)
@api_route(Methods.Get, detail_endpoint)
def events_event_id_get(event_id: str):
    """Gets an event by its id."""
    return json.dumps({})


@api_parameter(ParameterTypes.Path, 'eventId', str, data_format=StringFormats.Uuid, description='Id of the event.')
@api_response(HTTPStatus.NO_CONTENT)
@api_response(HTTPStatus.NOT_FOUND)
@api_response(HTTPStatus.BAD_REQUEST)
@api_response(HTTPStatus.INTERNAL_SERVER_ERROR)
@api_route(Methods.Put, detail_endpoint, Event)
def events_event_id_put(event_id: str, body: Dict = None):
    """Updates an event by its id."""
    # data: Event = Event.from_dict(body)
    # if event_id != data.id:
    #     return 'id mismatch', 400

    return '', 204
