from typing import List, Generic, TypeVar
from src.openapi_annotations import api_model, api_property

ModelType = TypeVar('ModelType')


@api_model
class Page(Generic[ModelType]):
    """A slice of data returned."""
    def __init__(self, data: List[ModelType] = None, total: int = 0, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._data = [] if data is None else data
        self._total = total

    @property
    def total(self) -> int:
        return self._total

    @total.setter
    @api_property()
    def total(self, total: int):
        """The total amount of records on the backend."""
        self._total = total

    @property
    def data(self) -> List[ModelType]:
        return self._data

    @data.setter
    @api_property()
    def data(self, data: List[ModelType]):
        """A list of records."""
        self._data = data
