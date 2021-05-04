from src.openapi_annotations import api_model, api_property, StringFormats


@api_model
class MyModel:
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
