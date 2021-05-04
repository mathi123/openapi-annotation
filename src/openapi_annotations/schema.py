
class Schema:
    def __init__(self,
                 data_type: type = str,
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
                 items_schema: 'Schema' = None):
        self._data_type = data_type
        self._data_format = data_format
        self._min_length = min_length
        self._max_length = max_length
        self._required = required
        self._enum = enum
        self._description = description
        self._minimum = minimum
        self._maximum = maximum
        self._exclusive_minimum = exclusive_minimum
        self._exclusive_maximum = exclusive_maximum
        self._items_schema = items_schema

    def to_dict(self):
        return {
            'data_type': self._data_type,
            'data_format': self._data_format,
            'min_length': self._min_length,
            'max_length': self._max_length,
            'required': self._required,
            'enum': self._enum,
            'description': self._description,
            'minimum': self._minimum,
            'maximum': self._maximum,
            'exclusive_minimum': self._exclusive_minimum,
            'exclusive_maximum': self._exclusive_maximum,
            'items_schema': self._items_schema.to_dict() if self._items_schema is not None else None
        }
