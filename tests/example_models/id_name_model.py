from src.openapi_annotations import api_model, api_property
from .id_model import IdModel


@api_model
class IdNameModel(IdModel):
    def __init__(self, id: str = None, name: str = None, *args, **kwargs):
        super().__init__(id=id, *args, **kwargs)
        self._name = name

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    @api_property(nullable=True)
    def name(self, name: str):
        """Human readable name."""
        self._name = name
