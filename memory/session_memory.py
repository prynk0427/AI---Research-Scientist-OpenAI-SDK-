from dataclasses import dataclass, field
from typing import Any


@dataclass
class SessionMemory:
    """Short-term research memory shared by the Streamlit session."""

    data: dict[str, Any] = field(default_factory=dict)

    def save(self, key: str, value: Any) -> None:
        self.data[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        return self.data.get(key, default)

    def update(self, values: dict[str, Any]) -> None:
        self.data.update(values)

    def keys(self) -> list[str]:
        return list(self.data.keys())

    def clear(self) -> None:
        self.data.clear()
