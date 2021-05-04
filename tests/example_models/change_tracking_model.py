from datetime import datetime
from src.openapi_annotations import api_model, api_property, StringFormats


@api_model
class ChangeTrackingModel:
    """The timestamps of changes to this object are kept track of."""
    def __init__(self, created_at: datetime = None, modified_at: datetime = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._modified_at = modified_at
        self._created_at = created_at

    @property
    def created_at(self) -> datetime:
        return self._created_at

    @created_at.setter
    @api_property(nullable=True)
    def created_at(self, created_at: datetime):
        """The date this object was created. Cannot be modified."""
        self._created_at = created_at

    @property
    def modified_at(self) -> datetime:
        return self._modified_at

    @modified_at.setter
    @api_property(nullable=True)
    def modified_at(self, modified_at: datetime):
        """The date this object was last modified. This property is automatically updated."""
        self._modified_at = modified_at
