from src.openapi_annotations import api_model, api_property

@api_model
class ParentModel:
    @property
    def base_property(self) -> str:
        return self._base_property
    
    @base_property.setter
    @api_property()
    def base_property(self, value: str):
        self._base_property = value
