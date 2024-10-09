from dataclasses import dataclass

from pyeqx.core.common import from_str
from pyeqx.core.models.module.properties.data_module_properties import (
    DataModuleProperties,
)


@dataclass
class StreamDataModuleProperties(DataModuleProperties):
    name: str

    def __init__(self, storage: str, name: str):
        parsed_obj = {
            "name": name,
        }
        super().__init__(storage, parsed_obj)

    @staticmethod
    def from_dict(obj: dict) -> "StreamDataModuleProperties":
        assert isinstance(obj, dict)
        storage = from_str(obj.get("storage"))
        name = from_str(obj.get("name"))
        return StreamDataModuleProperties(storage, name)

    def to_dict(self) -> dict:
        result = super().to_dict()
        result.update({"name": self.name})
        return result

    def from_properties(self) -> "StreamDataModuleProperties":
        return StreamDataModuleProperties(self.storage, self.name)
