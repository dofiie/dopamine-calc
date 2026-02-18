"""Utility helpers for validation, input handling, formatting, and styling."""

from __future__ import annotations

from datetime import date
from typing import Callable


# ======================
# 🎨 Terminal Colors
# ======================

class Color:
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    CYAN = "\033[96m"
    MAGENTA = "\033[95m"
    BOLD = "\033[1m"
    RESET = "\033[0m"


def today_iso() -> str:
    """Return today's date as YYYY-MM-DD."""
    return date.today().isoformat()


def clamp(value: float, lower: float, upper: float) -> float:
    """Clamp a numeric value into a closed range."""
    return max(lower, min(upper, value))


def validate_non_negative(name: str, value: float) -> None:
    """Raise ValueError if value is negative."""
    if value < 0:
        raise ValueError(f"{name} cannot be negative")


def validate_score(name: str, value: int) -> None:
    """Validate integer score in range 1-10."""
    if value < 1 or value > 10:
        raise ValueError(f"{name} must be between 1 and 10")


def validate_sleep(hours: float) -> None:
    """Validate sleep range."""
    if hours > 24:
        raise ValueError("Sleep cannot exceed 24 hours")
    validate_non_negative("Sleep", hours)


def prompt_value(prompt: str, caster: Callable[[str], float | int]) -> float | int:
    """Prompt until a valid value is parsed."""
    while True:
        raw = input(prompt).strip()
        try:
            return caster(raw)
        except ValueError:
            print("Invalid input. Please try again.")


def float_fmt(value: float) -> str:
    """Format floating-point values consistently."""
    return f"{value:.2f}"

def progress_bar(value: float, max_value: float = 10, width: int = 30) -> str:
    """Generate ASCII progress bar."""
    ratio = max(0, min(value / max_value, 1))
    filled = int(ratio * width)
    bar = "█" * filled + "-" * (width - filled)
    return f"[{bar}] {value:.2f}/{max_value}"
