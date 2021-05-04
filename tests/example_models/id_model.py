from src.openapi_annotations import api_model, api_property, StringFormats

@api_model
class IdModel:
    def __init__(self, id: str = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._id = id

    @property
    def id(self) -> str:
        return self._id

    @id.setter
    @api_property(data_format=StringFormats.Uuid, nullable=True)
    def id(self, id: str):
        """Unique ID of this object."""
        self._id = id
