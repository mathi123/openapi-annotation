
from .globals import api_routes, api_models
from .parameter_types import ParameterTypes
from .string_formats import StringFormats
from datetime import datetime
from typing import List, Dict, _GenericAlias


def _create_new_model_from_generic(generic_model, type_instance):
    type_instance_name = type_instance.__name__
    new_model_name = '{}{}'.format(type_instance_name, generic_model['name'])
    existing = list(filter(lambda x: x['name'] == new_model_name, api_models))
    if len(existing) > 0:
        return new_model_name

    new_model = {
        'bases': [],
        'module': generic_model['module'],
        'name': new_model_name,
        'description': generic_model['description'],
        'referenced_from_root': True,
        'attributes': []
    }
    for attr in generic_model['attributes']:
        copy = {}
        for key in attr.keys():
            copy[key] = attr[key]

        if copy['data_type'].__module__ == 'typing' and copy['data_type']._name == 'List':
            if str(copy['data_type'].__args__[0]).index(generic_model['generic_type_vars'][0]) > 0:
                copy['data_type'] = List[type_instance]

        new_model['attributes'].append(copy)

    api_models.append(new_model)
    return new_model_name


def _get_component_schema_ref(model):
    if isinstance(model, _GenericAlias):
        name = str(model)
        generic_module_name = model.__module__
        generic_name = name[len(generic_module_name)+1:name.index('[')]
        generic_args = model.__args__[0]
        generic_model = list(filter(lambda x: x['module'] == generic_module_name and
                                    x['name'] == generic_name, api_models))[0]
        new_name = _create_new_model_from_generic(generic_model, generic_args)
        return '#/components/schemas/{}'.format(new_name)
    return '#/components/schemas/{}'.format(model.__name__)


def _add_response_model(spec, response, default_response_descriptions):
    response_spec = {
    }
    if response['description'] is not None:
        response_spec['description'] = response['description']
    elif response['status_code'] in default_response_descriptions:
        response_spec['description'] = default_response_descriptions[response['status_code']]
    if response['model'] is not None:
        response_spec['content'] = {
            '*/*': {
                'schema': {
                    '$ref': _get_component_schema_ref(response['model'])
                }
            }
        }
    spec['responses'][str(response['status_code'].value)] = response_spec


def _is_array_type(model_type: type):
    return model_type is not None and (model_type == list or (model_type.__module__ == 'typing' and
                                                              model_type._name == 'List'))


def _get_array_type(model_type: type):
    if model_type == list:
        return str
    elif model_type.__module__ == 'typing' and model_type._name == 'List':
        return model_type.__args__[0] if len(model_type.__args__) == 1 else str
    raise Exception('Cannot get array type for array {}'.format(model_type))


def _is_api_model(model_type: type):
    return not (model_type == str or model_type == datetime or
                model_type == int or model_type == float or model_type == bool
                or model_type == dict or model_type == Dict or _is_array_type(model_type))


def _convert_type_to_string(model_type: type):
    if model_type == str or model_type == datetime:
        return 'string'
    elif model_type == int:
        return 'integer'
    elif model_type == float:
        return 'number'
    elif model_type == bool:
        return 'boolean'
    elif _is_array_type(model_type):
        return 'array'
    elif model_type == dict or model_type == Dict:
        return 'object'
    raise Exception('Could not generate type for {}'.format(model_type))


def _create_schema(parameter, property_mode, root_ref: bool):
    if parameter['data_type'] is not None and _is_api_model(parameter['data_type']):
        api_model = list(filter(lambda x: x['module'] == parameter['data_type'].__module__ and
                                x['name'] == parameter['data_type'].__name__, api_models))[0]
        if 'referenced_from_root' not in api_model or not api_model['referenced_from_root']:
            api_model['referenced_from_root'] = root_ref
        return {
            '$ref': '#/components/schemas/{}'.format(api_model['name'])
        }
    if 'schema' in parameter and parameter['schema'] is not None:
        return _create_schema(parameter['schema'].to_dict(), property_mode, root_ref)
    param_spec = {
        'type': _convert_type_to_string(parameter['data_type'])
    }
    if property_mode and 'description' in parameter and parameter['description'] is not None:
        param_spec['description'] = parameter['description']
    if parameter['data_format'] is not None:
        param_spec['format'] = parameter['data_format']
    elif parameter['data_type'] == datetime:
        param_spec['format'] = StringFormats.Datetime
    if not property_mode and parameter['required'] is not None:
        param_spec['required'] = parameter['required']
    if parameter['min_length'] is not None:
        param_spec['minLength'] = parameter['min_length']
    if parameter['max_length'] is not None:
        param_spec['maxLength'] = parameter['max_length']
    if parameter['minimum'] is not None:
        param_spec['minimum'] = parameter['minimum']
    if parameter['maximum'] is not None:
        param_spec['maximum'] = parameter['maximum']
    if parameter['exclusive_minimum'] is not None:
        param_spec['exclusiveMinimum'] = parameter['exclusive_minimum']
    if parameter['exclusive_maximum'] is not None:
        param_spec['exclusiveMaximum'] = parameter['exclusive_maximum']
    if parameter['enum'] is not None and len(parameter['enum']) > 0:
        param_spec['enum'] = parameter['enum']
    if 'items_schema' in parameter and parameter['items_schema'] is not None:
        param_spec['items'] = _create_schema(
            parameter['items_schema'], property_mode, root_ref)
    elif _is_array_type(parameter['data_type']):
        array_type = _get_array_type(parameter['data_type'])
        if _is_api_model(array_type):
            api_model = list(filter(lambda x: x['module'] == array_type.__module__ and
                                    x['name'] == array_type.__name__, api_models))
            if len(api_model) > 0:
                param_spec['items'] = {
                    '$ref': '#/components/schemas/{}'.format(api_model[0]['name'])
                }
            else:
                param_spec['items'] = {
                    'type': 'object'
                }
        else:
            param_spec['items'] = {
                'type': _convert_type_to_string(array_type)
            }
    return param_spec


def _add_parameter(spec, parameter, default_parameter_descriptions):
    param_spec = {
        'name': parameter['name'],
        'in': parameter['type']
    }
    if parameter['required'] or parameter['type'] == ParameterTypes.Path:
        param_spec['required'] = True
    if parameter['description'] is not None:
        param_spec['description'] = parameter['description']
    elif parameter['name'] in default_parameter_descriptions:
        param_spec['description'] = default_parameter_descriptions[parameter['name']]
    param_spec['schema'] = _create_schema(parameter, False, False)

    spec['parameters'].append(param_spec)


def _build_route_spec(spec, path, routes, default_response_descriptions, default_parameter_descriptions):
    route_spec = {
    }
    for route in routes:
        route_method_spec = {
            'operationId': route['operation_id']
        }
        if route['description'] is not None:
            route_method_spec['description'] = route['description']
        if route['tag'] is not None:
            route_method_spec['tags'] = []
        if len(route['parameters']) > 0:
            route_method_spec['parameters'] = []
        if len(route['responses']) > 0:
            route_method_spec['responses'] = {}
        if route['body'] is not None:
            req_model = route['body'].__name__
            route_method_spec['requestBody'] = {
                '$ref': '#/components/requestBodies/{}'.format(req_model)
            }
            if req_model not in spec['components']['requestBodies']:
                spec['components']['requestBodies'][req_model] = {
                    'content': {
                        'application/json': {
                            'schema': {
                                '$ref': '#/components/schemas/{}'.format(req_model)
                            }
                        }
                    }
                }

        for parameter in route['parameters']:
            _add_parameter(route_method_spec, parameter,
                           default_parameter_descriptions)
        for response in route['responses']:
            _add_response_model(route_method_spec, response,
                                default_response_descriptions)
        route_spec[route['method'].lower()] = route_method_spec
    spec['paths'][path] = route_spec


def _build_route_specs(spec, default_response_descriptions, default_parameter_descriptions):
    distinct_paths = []
    for route in api_routes:
        if route['route'] not in distinct_paths:
            distinct_paths.append(route['route'])

    for distinct_path in distinct_paths:
        routes = list(
            filter(lambda x: x['route'] == distinct_path, api_routes))
        _build_route_spec(spec, distinct_path, routes,
                          default_response_descriptions, default_parameter_descriptions)


def _build_attribute_spec(attribute, root_ref: bool):
    param_spec = _create_schema(attribute, True, root_ref)

    return param_spec


def _build_attribute_list(model, attributes, camel_case: bool, root_ref: bool):
    for base in model['bases']:
        base_model = list(filter(lambda x: x['name'] == base['name'] and
                                 x['module'] == base['module'], api_models))[0]
        _build_attribute_list(base_model, attributes, camel_case, root_ref)

    for attribute in model['attributes']:
        name = attribute['name']
        if camel_case and '_' in name:
            temp = name.split('_')
            name = temp[0] + ''.join(ele.title() for ele in temp[1:])

        attributes[name] = _build_attribute_spec(attribute, root_ref)

    return attributes


def _build_model_spec(model, camel_case: bool, root_ref: bool):
    spec = {
        'type': 'object'
    }
    if 'referenced_from_root' not in model or not model['referenced_from_root']:
        model['referenced_from_root'] = root_ref

    if model['description'] is not None:
        spec['description'] = model['description']
    spec['properties'] = _build_attribute_list(model, {}, camel_case, root_ref)
    # required_attributes = list(map(lambda x: x['name'], filter(
    #     lambda x: x['required'] == True, model['attributes'])))
    # if len(required_attributes) > 0:

    return spec


def _build_model_specs(specs, camel_case: bool, all_models: bool):
    model_specs = {}
    for model in api_models:
        model_spec = _build_model_spec(
            model, camel_case, model['name'] in specs['components']['requestBodies'])
        model_specs[model['name']] = model_spec

    for model in api_models:
        if model['referenced_from_root'] or all_models:
            specs['components']['schemas'][model['name']
                                           ] = model_specs[model['name']]


def get_spec(title: str, version='1.0.0',
             camel_case: bool = False,
             all_models: bool = False,
             tags: list = None,
             externalDocs: dict = None,
             default_response_descriptions={},
             default_parameter_descriptions={}):
    spec = {
        'openapi': '3.0.0',
        'info': {
            'title': title,
            'version': version
        }
    }
    if tags is not None and len(tags) > 0:
        spec['tags'] = tags
    if externalDocs is not None:
        spec['externalDocs'] = externalDocs
    spec['paths'] = {}
    spec['components'] = {
        'requestBodies': {},
        'schemas': {}
    }
    _build_route_specs(spec, default_response_descriptions,
                       default_parameter_descriptions)
    _build_model_specs(spec, camel_case, all_models)
    return spec
