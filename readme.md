# OpenAPI Python annotations

Generate OpenApi with code-first annotations. Use type-hint info and docstrings to document your API. This is an experimental library!

## Getting Started

### Install the package

```
pip install openapi-annotations
```

### Document a model


```python
from openapi_annotations import api_model, api_property, StringFormats


@api_model
class Event:
    """The first model from this API."""

    @property
    def id(self) -> str:
        return self._id

    @id.setter
    @api_property(data_format=StringFormats.Uuid, nullable=True)
    def id(self, value: str):
        """The id of the object."""
        self._id = value

    @property
    def documented_property(self) -> str:
        return self._documented_property

    @documented_property.setter
    @api_property()
    def documented_property(self, value: str):
        """Property documentation."""
        self._documented_property = value
```


### Document a route


```python
from openapi_annotations import api_route, api_response
from http import HTTPStatus
from .models import Event # My custom model


@api_response(HTTPStatus.CREATED, Event)
@api_response(HTTPStatus.BAD_REQUEST)
@api_response(HTTPStatus.INTERNAL_SERVER_ERROR)
@api_route(Methods.Post, f'events/{{eventId}}', Event)
def events_post(body=None):
    """Creates a new event and returns it."""
    result = {}
    return json.dumps(result), 201

```


### View the swagger:

```python
import .controllers # Make sure you import all files containing annotations
from openapi_annotations import get_spec
import json

with open('./openapi.json', 'w') as file:
    file.write(json.dumps(spec, indent=4))
```
