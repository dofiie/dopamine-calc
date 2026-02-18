# 🧠 DOP — Offline Dopamine Optimization CLI

DOP is a fully offline behavioral analytics engine built in Python.

It tracks daily cognitive inputs (sleep, coffee, cigarettes, etc.) and mental outputs (focus, mood, energy), then computes performance metrics, detects patterns, and predicts future outcomes.

This is not a habit tracker.
It is a personal nervous-system diagnostic console.

---

# 🚀 Features

- Fully offline (no APIs, no cloud)
- Atomic JSON storage with corruption recovery
- Clean modular architecture
- Dopamine Efficiency Score (DES)
- Dopamine Load Score (DLS)
- ASCII performance visualization
- Sleep debt detection
- Crash risk prediction
- Weekly analytics with correlations
- Optimal performance zone detection
- Weighted similarity prediction engine

---

# 📊 Core Concepts

## Dopamine Efficiency Score (DES)

Measures cognitive performance efficiency.

Based on:
- Focus
- Mood
- Energy
- Sleep
- Coffee (penalty)
- Cigarettes (penalty)

Range: 0–10

High DES = efficient brain  
Low DES = overstimulated or sleep-deprived system  

---

## Dopamine Load Score (DLS)

Measures total stimulation input.

Formula:

DLS = coffee + cig + gaming

High DLS does NOT mean high performance.

You want:
Moderate DLS + High DES

---

## Sleep Debt

Calculates accumulated sleep deficit over last 7 entries.

Helps detect:
- Chronic fatigue
- Performance instability
- Cognitive decline risk

---

## Crash Risk Prediction

Predicts next-day cognitive crash risk using:

- Sleep level
- Stimulation load
- Cigarettes
- Coffee

Outputs:
- LOW
- MODERATE
- HIGH

---

# 🖥 Commands

Run using:
Make sure to run in `Dopamine Calc` folder
python -m dop.main <command>

Available commands:

- e        Log daily entry
- s        Show today’s summary
- w        Weekly analysis
- o        Detect optimal performance zones
- predict  Predict mood & focus from hypothetical inputs

---

# 🧪 Example Usage

Log a new entry:

python -m dop.main e

Weekly analysis:

python -m dop.main w

Optimal zone detection:

python -m dop.mail o

Prediction mode:

python -m dop predict

---

# 📁 Project Structure
```
dop/
│
├── main.py
├── analytics.py
├── storage.py
├── models.py
├── utils.py
└── data.json
```
Architecture Layers:

- CLI Layer → main.py
- Business Logic → analytics.py
- Persistence Layer → storage.py
- Data Model → models.py
- Utilities → utils.py

---

# 🛠 Requirements

- Python 3.11+
- No external dependencies

---

# 🧠 Philosophy

Track stimulus → Measure output → Detect patterns → Optimize behavior.

Treat your cognitive state like a system.
Tune performance intentionally.

---

# 🔮 Future Improvements

- SQLite backend
- ASCII weekly trend graphs
- Adaptive DES weighting
- Export to CSV
- Encrypted storage
- Hardcore discipline mode

---

# ⚠ Disclaimer

This tool does not provide medical advice.
It is designed for personal behavioral tracking and experimentation.

---

# 📌 Status

Actively evolving.
Modular and extensible.
Built for long-term behavioral insight.
