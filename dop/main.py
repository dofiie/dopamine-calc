"""CLI entrypoint for DOP (Offline Dopamine Optimization CLI)."""
from __future__ import annotations

import argparse
from datetime import date, timedelta

from dop.models import Entry

from dop.analytics import (
    average,
    calculate_des,
    calculate_dls,
    detect_flags,
    detect_optimal_zone,
    pearson_correlation,
    predict_from_history,
    calculate_focus,
    calculate_mood,
    calculate_energy,
    detect_sleep_debt,
    predict_crash_risk,
)

from dop.storage import (
    StorageError,
    add_entry,
    get_entry_by_date,
    load_entries,
    remove_entry_by_date,
)

from dop.utils import (
    Color,
    progress_bar,
    float_fmt,
    prompt_value,
    today_iso,
    validate_non_negative,
    validate_score,
    validate_sleep,
)


def prompt_entry() -> Entry:
    """Prompt user for behavioral-based entry."""

    print("\nEnter today's data:\n")

    # =====================
    # Stimulus Inputs
    # =====================
    coffee = int(prompt_value("Coffee cups: ", int))
    cig = int(prompt_value("Cigarettes: ", int))
    sleep = float(prompt_value("Sleep hours: ", float))
    gaming = float(prompt_value("Gaming hours: ", float))
    coding = float(prompt_value("Coding hours: ", float))

    validate_non_negative("Coffee", coffee)
    validate_non_negative("Cigarettes", cig)
    validate_sleep(sleep)
    validate_non_negative("Gaming", gaming)
    validate_non_negative("Coding", coding)

    print("\n--- Behavioral Assessment ---")

    # =====================
    # Focus Behavioral Inputs
    # =====================
    print("\nFocus Assessment:")
    print("Deep Work Capability:")
    print("0 = Couldn't focus")
    print("1 = Some focus")
    print("2 = Deep focus possible")
    deep_work = int(prompt_value("Select (0-2): ", int))

    print("Distraction Level:")
    print("0 = Constantly distracted")
    print("1 = Sometimes distracted")
    print("2 = Rarely distracted")
    distraction = int(prompt_value("Select (0-2): ", int))

    # =====================
    # Mood Behavioral Inputs
    # =====================
    print("\nMood Assessment:")
    print("Emotional Stability:")
    print("0 = Irritable / unstable")
    print("1 = Normal")
    print("2 = Calm / positive")
    stability = int(prompt_value("Select (0-2): ", int))

    print("Satisfaction With Day:")
    print("0 = Bad day")
    print("1 = Neutral")
    print("2 = Good day")
    satisfaction = int(prompt_value("Select (0-2): ", int))

    # =====================
    # Energy Behavioral Inputs
    # =====================
    print("\nEnergy Assessment:")
    print("Physical Fatigue:")
    print("0 = Exhausted")
    print("1 = Normal")
    print("2 = Energized")
    fatigue = int(prompt_value("Select (0-2): ", int))

    print("Mental Sharpness:")
    print("0 = Foggy")
    print("1 = Normal")
    print("2 = Sharp")
    sharpness = int(prompt_value("Select (0-2): ", int))

    # =====================
    # Calculate Derived Scores
    # =====================
    focus = calculate_focus(deep_work, distraction)
    mood = calculate_mood(stability, satisfaction)
    energy = calculate_energy(fatigue, sharpness)

    des = calculate_des(focus, mood, energy, sleep, coffee, cig)
    dls = calculate_dls(coffee, cig, gaming)

    return Entry(
        date=today_iso(),
        coffee=coffee,
        cig=cig,
        sleep=sleep,
        gaming=gaming,
        coding=coding,
        mood=mood,
        focus=focus,
        energy=energy,
        des=des,
        dls=dls,
    )


def print_entry_summary(entry: Entry, title: str = "System Report") -> None:
    """Print full styled system diagnostic report for an entry."""

    print(f"\n{Color.CYAN}{Color.BOLD}══════════ DOP SYSTEM REPORT ══════════{Color.RESET}")
    print(f"{Color.MAGENTA}{title} ({entry.date}){Color.RESET}")

    # ======================
    # Inputs
    # ======================
    print("\nInputs:")
    print(
        f"  Coffee: {entry.coffee} | Cigarettes: {entry.cig} | "
        f"Sleep: {float_fmt(entry.sleep)}h | "
        f"Gaming: {float_fmt(entry.gaming)}h | "
        f"Coding: {float_fmt(entry.coding)}h"
    )

    # ======================
    # Outputs
    # ======================
    print("\nOutputs:")
    print(
        f"  Mood: {entry.mood}/10 | "
        f"Focus: {entry.focus}/10 | "
        f"Energy: {entry.energy}/10"
    )

    # ======================
    # Scores
    # ======================
    print("\nScores:")

    print(
        f"\nDopamine Efficiency Score (DES):"
    )
    print(
        f"{Color.CYAN}{progress_bar(entry.des)}{Color.RESET}"
    )

    print(
        f"\nDopamine Load Score (DLS): "
        f"{Color.YELLOW}{float_fmt(entry.dls)}{Color.RESET}"
    )

    # ======================
    # Efficiency Interpretation
    # ======================
    if entry.des >= 8:
        print(f"\n{Color.GREEN}Status: LOCKED IN — High cognitive efficiency.{Color.RESET}")
    elif entry.des >= 5:
        print(f"\n{Color.YELLOW}Status: Stable — Room for optimization.{Color.RESET}")
    else:
        print(f"\n{Color.RED}Status: Low Efficiency — Improve sleep or reduce overstimulation.{Color.RESET}")

    # ======================
    # Stimulation Interpretation
    # ======================
    if entry.dls >= 8:
        print(f"{Color.RED}Stimulation Level: High — Risk of overstimulation.{Color.RESET}")
    elif entry.dls >= 4:
        print(f"{Color.YELLOW}Stimulation Level: Moderate.{Color.RESET}")
    else:
        print(f"{Color.GREEN}Stimulation Level: Controlled.{Color.RESET}")

    # ======================
    # Sleep Debt Detection
    # ======================
    entries = load_entries()
    sleep_debt = detect_sleep_debt(entries)

    if sleep_debt > 0:
        print(
            f"\n{Color.RED}Sleep Debt (Last 7 Days): "
            f"{sleep_debt:.2f} hours owed{Color.RESET}"
        )
    else:
        print(
            f"\n{Color.GREEN}Sleep Debt: Cleared{Color.RESET}"
        )

    # ======================
    # Next-Day Crash Risk
    # ======================
    risk = predict_crash_risk(entry)

    if risk == "HIGH":
        print(f"{Color.RED}Next-Day Crash Risk: HIGH ⚠{Color.RESET}")
    elif risk == "MODERATE":
        print(f"{Color.YELLOW}Next-Day Crash Risk: MODERATE{Color.RESET}")
    else:
        print(f"{Color.GREEN}Next-Day Crash Risk: LOW{Color.RESET}")

    # ======================
    # Behavioral Alerts
    # ======================
    flags = detect_flags(entry)
    if flags:
        print(f"\n{Color.RED}Alerts:{Color.RESET}")
        for flag in flags:
            print(f"  - {flag}")

    print(f"{Color.CYAN}{Color.BOLD}═══════════════════════════════════════{Color.RESET}\n")


def handle_entry() -> None:
    """Command handler for `dop e` with view/overwrite/cancel logic."""

    today = today_iso()
    existing = get_entry_by_date(today)

    if existing:
        print(f"\nEntry already exists for date {today}.")
        print("1) View")
        print("2) Overwrite")
        print("3) Cancel")

        while True:
            choice = input("Select (1-3): ").strip()

            if choice == "1":
                print_entry_summary(existing, "Existing Entry")
                return

            elif choice == "2":
                print("\nOverwriting existing entry...\n")
                remove_entry_by_date(today)
                break

            elif choice == "3":
                print("Cancelled.")
                return

            else:
                print("Invalid selection. Please choose 1, 2, or 3.")

    # If no existing entry OR overwrite selected
    entry = prompt_entry()
    add_entry(entry)
    print_entry_summary(entry, "Entry saved")



def handle_summary() -> None:
    """Command handler for `dop s`."""
    entry = get_entry_by_date(today_iso())
    if not entry:
        print("No entry found for today. Use `dop e` first.")
        return
    print_entry_summary(entry, "Today's summary")


def handle_weekly() -> None:
    """Command handler for `dop w`."""
    entries = load_entries()
    if not entries:
        print("No data available for weekly analysis.")
        return

    last_7 = { (date.today() - timedelta(days=offset)).isoformat() for offset in range(7) }
    weekly_entries = [entry for entry in entries if entry.date in last_7]
    if not weekly_entries:
        print("No entries in the last 7 days.")
        return

    moods = [entry.mood for entry in weekly_entries]
    focuses = [entry.focus for entry in weekly_entries]
    des_values = [entry.des for entry in weekly_entries]
    sleeps = [entry.sleep for entry in weekly_entries]
    coffees = [entry.coffee for entry in weekly_entries]
    cigs = [entry.cig for entry in weekly_entries]

    print("\n=== Weekly Analysis ===")
    print(f"Entries analyzed: {len(weekly_entries)}")
    print(f"Average mood: {float_fmt(average(moods))}")
    print(f"Average focus: {float_fmt(average(focuses))}")
    print(f"Average DES: {float_fmt(average(des_values))}")
    print(f"Sleep vs Focus correlation: {float_fmt(pearson_correlation(sleeps, focuses))}")
    print(f"Coffee vs Focus correlation: {float_fmt(pearson_correlation(coffees, focuses))}")
    print(f"Cig vs Focus correlation: {float_fmt(pearson_correlation(cigs, focuses))}")


def handle_optimal() -> None:
    """Command handler for `dop o`."""
    entries = load_entries()
    if not entries:
        print("No historical data available.")
        return

    recommendations = detect_optimal_zone(entries)
    print("\n=== Optimal Zone Detection ===")
    print(f"Best coffee range for focus: {recommendations['coffee']}")
    print(f"Best sleep range for focus: {recommendations['sleep']}")
    print(f"Cigarette decline threshold: {recommendations['cig_threshold']}")
    print(f"Minimum sleep for stable mood: {recommendations['stable_mood_sleep']}")


def handle_predict() -> None:
    """Command handler for `dop predict`."""
    entries = load_entries()

    print("\nProvide hypothetical inputs:")
    coffee = int(prompt_value("Coffee cups: ", int))
    cig = int(prompt_value("Cigarettes: ", int))
    sleep = float(prompt_value("Sleep hours: ", float))
    gaming = float(prompt_value("Gaming hours: ", float))

    validate_non_negative("Coffee", coffee)
    validate_non_negative("Cigarettes", cig)
    validate_sleep(sleep)
    validate_non_negative("Gaming", gaming)

    prediction = predict_from_history(entries, coffee, cig, sleep, gaming)
    print("\n=== Prediction ===")
    print(f"Likely focus: {float_fmt(prediction['focus'])}/10")
    print(f"Likely mood: {float_fmt(prediction['mood'])}/10")


def build_parser() -> argparse.ArgumentParser:
    """Build and return argparse parser."""
    parser = argparse.ArgumentParser(prog="dop", description="Offline Dopamine Optimization CLI")
    parser.add_argument(
        "command",
        choices=["e", "s", "w", "o", "predict"],
        help="e=entry, s=summary, w=weekly, o=optimal, predict=prediction",
    )
    return parser


def main() -> None:
    """CLI main function."""
    parser = build_parser()
    args = parser.parse_args()

    try:
        if args.command == "e":
            handle_entry()
        elif args.command == "s":
            handle_summary()
        elif args.command == "w":
            handle_weekly()
        elif args.command == "o":
            handle_optimal()
        elif args.command == "predict":
            handle_predict()
    except (StorageError, ValueError) as err:
        print(f"Error: {err}")


if __name__ == "__main__":
    main()
