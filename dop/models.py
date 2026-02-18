"""Data models for the DOP CLI application."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(slots=True)
class Entry:
    """Represents one daily behavioral analytics record."""

    date: str
    coffee: int
    cig: int
    sleep: float
    gaming: float
    coding: float
    mood: int
    focus: int
    energy: int
    des: float
    dls: float

    def to_dict(self) -> dict[str, Any]:
        """Serialize an entry to a JSON-compatible dictionary."""
        payload = asdict(self)
        payload["sleep"] = round(self.sleep, 2)
        payload["gaming"] = round(self.gaming, 2)
        payload["coding"] = round(self.coding, 2)
        payload["des"] = round(self.des, 2)
        payload["dls"] = round(self.dls, 2)
        return payload

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Entry":
        """Create an entry from persisted JSON payload."""
        return cls(
            date=str(data["date"]),
            coffee=int(data["coffee"]),
            cig=int(data["cig"]),
            sleep=float(data["sleep"]),
            gaming=float(data["gaming"]),
            coding=float(data["coding"]),
            mood=int(data["mood"]),
            focus=int(data["focus"]),
            energy=int(data["energy"]),
            des=float(data["des"]),
            dls=float(data["dls"]),
        )
