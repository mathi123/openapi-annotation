from .id_name_model import IdNameModel
from .change_tracking_model import ChangeTrackingModel
from typing import List
from datetime import datetime
from src.openapi_annotations import api_model, api_property


@api_model
class Event(IdNameModel, ChangeTrackingModel):
    """An event documents an interesting occurence that can be useful in trend analytics. Events can be used to annotate trend charts"""

    def __init__(self, id_data: str = None, name: str = None):
        super().__init__(id=id_data, name=name)
        self._starts_at = None
        self._ends_at = None
        self._description = None
        self._labels = None
        self._types = None
        self._owner = None

    @property
    def ends_at(self) -> datetime:
        return self._ends_at

    @ends_at.setter
    @api_property(nullable=True)
    def ends_at(self, value: datetime):
        """In case the event took longer than one day, ends_at indicates the day the event finished."""
        self._ends_at = value

    @property
    def starts_at(self) -> datetime:
        return self._starts_at

    @starts_at.setter
    @api_property(required=True, nullable=False)
    def starts_at(self, value: datetime):
        """The day the event occured or started."""
        self._starts_at = value

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    @api_property(nullable=True)
    def description(self, description: str):
        """Plain text description of the event."""
        self._description = description

    @property
    def labels(self) -> List[str]:
        return self._labels

    @labels.setter
    @api_property(nullable=True)
    def labels(self, labels: List[str]):
        self._labels = labels

    @property
    def types(self) -> List[str]:
        return self._types

    @types.setter
    @api_property(nullable=True)
    def types(self, types: List[str]):
        """Indicates multiple categories this event falls under."""
        self._types = types

    @property
    @api_property(nullable=True)
    def owner(self) -> IdNameModel:
        return self._owner

    @owner.setter
    def owner(self, value: IdNameModel):
        """The user who created this event."""
        self._owner = value
