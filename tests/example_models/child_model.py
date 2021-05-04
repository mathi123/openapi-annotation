from .parent_model import ParentModel
from src.openapi_annotations import api_model, api_property

@api_model
class ChildModel(ParentModel):
    @property
    def child_property(self) -> str:
        return self._child_property
    
    @child_property.setter
    @api_property()
    def child_property(self, value: str):
        self._child_property = value
