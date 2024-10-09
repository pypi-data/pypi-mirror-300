from dataclasses import dataclass
from typing import Any

from pyeqx.core.common import from_str
from pyeqx.core.models.storage.properties.data_properties import DataProperties


@dataclass
class KafkaDataProperties(DataProperties):
    topic: str
    bootstrap_servers: str

    def __init__(self, topic, bootstrap_servers):
        parsed_obj = {
            "topic": topic,
            "bootstrapServers": bootstrap_servers,
        }
        super().__init__(parsed_obj)

    @staticmethod
    def from_dict(obj: Any) -> "KafkaDataProperties":
        assert isinstance(obj, dict)
        topic = from_str(obj.get("topic"))
        bootstrap_servers = from_str(obj.get("bootstrapServers"))
        return KafkaDataProperties(topic, bootstrap_servers)

    def to_dict(self) -> dict:
        result: dict = {}
        result["topic"] = from_str(self.topic)
        result["bootstrapServers"] = from_str(self.bootstrap_servers)
        return result

    def from_properties(self) -> "KafkaDataProperties":
        return KafkaDataProperties(self.topic, self.bootstrap_servers)
