"""Business analytics and scoring for DOP."""

from __future__ import annotations

from collections import defaultdict
from math import sqrt

from dop.models import Entry
from dop.utils import clamp

def detect_sleep_debt(entries: list[Entry], ideal_sleep: float = 7.0) -> float:
    """Calculate cumulative sleep debt over recent entries."""
    if not entries:
        return 0.0

    debt = 0.0
    for entry in entries[-7:]:  # last 7 entries
        if entry.sleep < ideal_sleep:
            debt += ideal_sleep - entry.sleep

    return round(debt, 2)


def calculate_des(
    focus: int,
    mood: int,
    energy: int,
    sleep: float,
    coffee: int,
    cig: int,
) -> float:
    """Compute Dopamine Efficiency Score (DES), clamped to [0, 10]."""
    des = (
        (focus * 0.4)
        + (mood * 0.3)
        + (energy * 0.3)
        + (sleep * 0.25)
        - (coffee * 0.2)
        - (cig * 0.3)
    )
    return round(clamp(des, 0, 10), 2)


def calculate_dls(coffee: int, cig: int, gaming: float) -> float:
    """Compute Dopamine Load Score (DLS)."""
    return round(coffee + cig + gaming, 2)


def detect_flags(entry: Entry, overstim_threshold: float = 8.0) -> list[str]:
    """Detect notable behavioral conditions for a single entry."""
    flags: list[str] = []
    if entry.sleep < 5 and entry.cig > 4 and entry.focus < 5:
        flags.append("Burnout risk detected: low sleep + high cigarettes + low focus.")
    if entry.dls > overstim_threshold:
        flags.append("Overstimulation warning: dopamine load is elevated.")
    if entry.des >= 8:
        flags.append("Locked-In mode: high cognitive efficiency today.")
    return flags


def average(values: list[float]) -> float:
    """Return arithmetic mean, or 0 when list is empty."""
    if not values:
        return 0.0
    return sum(values) / len(values)


def pearson_correlation(x_values: list[float], y_values: list[float]) -> float:
    """Compute Pearson correlation coefficient."""
    if len(x_values) != len(y_values) or len(x_values) < 2:
        return 0.0

    x_mean = average(x_values)
    y_mean = average(y_values)

    numerator = sum((x - x_mean) * (y - y_mean) for x, y in zip(x_values, y_values))
    x_var = sum((x - x_mean) ** 2 for x in x_values)
    y_var = sum((y - y_mean) ** 2 for y in y_values)

    denominator = sqrt(x_var * y_var)
    if denominator == 0:
        return 0.0

    return numerator / denominator


def _bucket_range(value: float, width: float) -> str:
    """Create range bucket labels like 4.0-5.9."""
    lower = int(value // width) * width
    upper = lower + width - 0.1
    return f"{lower:.1f}-{upper:.1f}"


def detect_optimal_zone(entries: list[Entry]) -> dict[str, str]:
    """Determine optimal behavioral zones from historical data."""
    if not entries:
        return {
            "coffee": "No data",
            "sleep": "No data",
            "cig_threshold": "No data",
            "stable_mood_sleep": "No data",
        }

    coffee_groups: dict[int, list[int]] = defaultdict(list)
    sleep_groups: dict[str, list[int]] = defaultdict(list)
    cig_groups: dict[int, list[int]] = defaultdict(list)

    for entry in entries:
        coffee_groups[entry.coffee].append(entry.focus)
        sleep_groups[_bucket_range(entry.sleep, 2.0)].append(entry.focus)
        cig_groups[entry.cig].append(entry.focus)

    best_coffee = max(coffee_groups.items(), key=lambda item: average(item[1]))
    best_sleep = max(sleep_groups.items(), key=lambda item: average(item[1]))

    sorted_cig = sorted(cig_groups.items(), key=lambda item: item[0])
    decline_threshold = "No clear threshold"
    baseline = average(sorted_cig[0][1]) if sorted_cig else 0
    for cig_count, focuses in sorted_cig[1:]:
        if average(focuses) < baseline - 1:
            decline_threshold = f">= {cig_count} cig/day"
            break

    stable_mood_entries = [entry for entry in entries if entry.mood >= 7]
    min_sleep = (
        min(entry.sleep for entry in stable_mood_entries)
        if stable_mood_entries
        else min(entry.sleep for entry in entries)
    )

    return {
        "coffee": f"{best_coffee[0]} cups/day",
        "sleep": f"{best_sleep[0]} hours",
        "cig_threshold": decline_threshold,
        "stable_mood_sleep": f"{min_sleep:.1f}h",
    }

def predict_crash_risk(entry: Entry) -> str:
    """
    Predict next-day crash risk based on overstimulation and sleep deficit.
    """
    risk_score = 0

    if entry.sleep < 5:
        risk_score += 2
    if entry.dls >= 8:
        risk_score += 2
    if entry.cig >= 4:
        risk_score += 1
    if entry.coffee >= 4:
        risk_score += 1

    if risk_score >= 4:
        return "HIGH"
    elif risk_score >= 2:
        return "MODERATE"
    else:
        return "LOW"


def predict_from_history(
    entries: list[Entry],
    coffee: int,
    cig: int,
    sleep: float,
    gaming: float,
) -> dict[str, float]:
    """Predict mood/focus using weighted similarity from historical records."""
    if not entries:
        return {"focus": 5.0, "mood": 5.0}

    weights_and_entries: list[tuple[float, Entry]] = []
    for entry in entries:
        distance = (
            abs(entry.coffee - coffee) * 1.2
            + abs(entry.cig - cig) * 1.4
            + abs(entry.sleep - sleep) * 0.8
            + abs(entry.gaming - gaming) * 0.7
        )
        weight = 1 / (1 + distance)
        weights_and_entries.append((weight, entry))

    top_neighbors = sorted(weights_and_entries, key=lambda pair: pair[0], reverse=True)[:5]
    total_weight = sum(weight for weight, _ in top_neighbors)
    if total_weight == 0:
        return {"focus": average([entry.focus for entry in entries]), "mood": average([entry.mood for entry in entries])}

    focus = sum(weight * item.focus for weight, item in top_neighbors) / total_weight
    mood = sum(weight * item.mood for weight, item in top_neighbors) / total_weight

    return {"focus": round(clamp(focus, 1, 10), 2), "mood": round(clamp(mood, 1, 10), 2)}
