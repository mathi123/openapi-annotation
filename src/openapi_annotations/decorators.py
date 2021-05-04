from .schema import Schema
from .globals import api_models, api_routes
from functools import wraps
from typing import get_type_hints, Generic
import logging
import inspect
import functools


logger = logging.getLogger(__name__)


def _get_model(module_name: str, name: str):
    filtered = list(
        filter(lambda x: x['name'] == name and x['module'] == module_name, api_models))
    return filtered[0] if len(filtered) > 0 else None


def _create_model(module_name: str, name: str):
    model = {
        'module': module_name,
        'name': name,
        'generic_type_vars': [],
        'attributes': []
    }
    api_models.append(model)
    return model


def _get_or_create_model(module_name: str, name: str):
    model = _get_model(module_name, name)
    if model is None:
        model = _create_model(module_name, name)
    return model


def _get_route(operation_id: str):
    filtered = list(
        filter(lambda x: x['operation_id'] == operation_id, api_routes))
    return filtered[0] if len(filtered) > 0 else None


def _create_route(operation_id: str):
    model = {
        'operation_id': operation_id,
        'parameters': [],
        'responses': []
    }
    api_routes.append(model)
    return model


def _get_or_create_route(operation_id: str):
    route = _get_route(operation_id)
    if route is None:
        route = _create_route(operation_id)
    return route


def api_model(model_class):
    model = _get_or_create_model(model_class.__module__, model_class.__name__)
    model['description'] = model_class.__doc__
    model['bases'] = []
    for base in model_class.__bases__:
        if base == Generic:
            model['generic_type_vars'] = list(
                map(lambda x: x.__name__, model_class.__parameters__))
        elif _get_model(base.__module__, base.__name__) is not None:
            model['bases'].append({
                'module': base.__module__,
                'name': base.__name__
            })

    return model_class


def api_property(
        json_name: str = None,
        data_format: str = None,
        min_length: int = None,
        max_length: int = None,
        required: bool = None,
        nullable: bool = None,
        enum: list = None,
        minimum: int = None,
        maximum: int = None,
        exclusive_minimum: bool = None,
        exclusive_maximum: bool = None,
        schema: Schema = None):
    def inner_function(function):
        model = _get_or_create_model(function.__module__, str(
            function).split(" ")[1].split(".")[0])
        attribute_name = function.__name__
        attribute = {
            'name': attribute_name,
            'description': function.__doc__,
            'json_name': json_name,
            'data_format': data_format,
            'min_length': min_length,
            'max_length': max_length,
            'required': required,
            'nullable': nullable,
            'minimum': minimum,
            'maximum': maximum,
            'exclusive_minimum': exclusive_minimum,
            'exclusive_maximum': exclusive_maximum,
            'enum': enum,
            'schema': schema
        }

        hints = get_type_hints(function)
        if len(hints) == 1:
            attribute['data_type'] = hints[list(hints.keys())[0]]

        model['attributes'].append(attribute)

        @wraps(function)
        def wrapper(*args, **kwargs):
            function(*args, **kwargs)
        return wrapper
    return inner_function


def api_response(status_code: int,
                 reponse_model: type = None,
                 description: str = None):
    def inner_function(function):
        operation_id = '{}.{}'.format(function.__module__, function.__name__)
        route = _get_or_create_route(operation_id)
        route['responses'].append({
            'status_code': status_code,
            'description': description,
            'model': reponse_model
        })

        @wraps(function)
        def wrapper(*args, **kwargs):
            function(*args, **kwargs)
        return wrapper
    return inner_function


def api_route(method: str,
              route: str,
              body_model: type = None,
              tag: str = None):
    def inner_function(function):
        operation_id = '{}.{}'.format(function.__module__, function.__name__)
        model = _get_or_create_route(operation_id)
        model['route'] = route
        model['method'] = method
        model['description'] = function.__doc__
        model['body'] = body_model
        model['tag'] = tag

        @wraps(function)
        def wrapper(*args, **kwargs):
            function(*args, **kwargs)
        return wrapper
    return inner_function


def api_parameter(
        parameter_type: str,
        name: str,
        data_type: type = None,
        data_format: str = None,
        min_length: int = None,
        max_length: int = None,
        required: bool = None,
        enum: list = None,
        description: str = None,
        minimum: int = None,
        maximum: int = None,
        exclusive_minimum: bool = None,
        exclusive_maximum: bool = None,
        schema: Schema = None):
    def inner_function(function):
        operation_id = '{}.{}'.format(function.__module__, function.__name__)
        model = _get_or_create_route(operation_id)
        model['parameters'].append({
            'name': name,
            'type': parameter_type,
            'data_type': data_type,
            'description': description,
            'data_format': data_format,
            'min_length': min_length,
            'max_length': max_length,
            'required': required,
            'minimum': minimum,
            'maximum': maximum,
            'exclusive_minimum': exclusive_minimum,
            'exclusive_maximum': exclusive_maximum,
            'schema': schema,
            'enum': enum
        })

        @wraps(function)
        def wrapper(*args, **kwargs):
            function(*args, **kwargs)
        return wrapper
    return inner_function
