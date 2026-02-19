# 🧠 DOP — Dopamine Optimization CLI

DOP is an offline behavioral analytics CLI that models cognitive performance using structured behavioral inputs instead of vague 1–10 ratings.

It tracks stimulation, sleep, behavioral focus quality, and emotional stability — then computes efficiency metrics, sleep debt, and crash risk prediction.

This is not a habit tracker.
It is a cognitive performance console.

---

## 🚀 Features

- Structured behavioral scoring (no arbitrary mood numbers)
- Dopamine Efficiency Score (DES)
- Dopamine Load Score (DLS)
- ASCII performance bar
- Sleep debt detection (7-day window)
- Next-day crash risk prediction
- Overwrite/View/Cancel flow for daily entries
- Fully offline
- Zero external dependencies

---

## 📊 Core Metrics

### Dopamine Efficiency Score (DES)
Measures cognitive output quality based on:
- Focus (behavioral)
- Mood (behavioral)
- Energy (behavioral)
- Sleep
- Stimulant penalties

Range: 0–10

---

### Dopamine Load Score (DLS)

Measures total stimulation load:

DLS = coffee + cigarettes + gaming

High DLS ≠ high performance.

---

### Sleep Debt

Tracks cumulative sleep deficit over last 7 entries.

---

### Crash Risk

Predicts next-day instability based on:
- Sleep level
- Stimulation load
- Cigarettes
- Coffee

Outputs: LOW / MODERATE / HIGH

---

## 🖥 Usage

Run with:

```
python -m dop e
```

Commands:

- `e` → Log daily entry
- `s` → Show today’s summary
- `w` → Weekly analysis
- `o` → Optimal zone detection
- `predict` → Hypothetical performance prediction

---

## 🧠 Philosophy

Track stimulus → Measure behavior → Detect patterns → Optimize system.

Treat your brain like a performance engine.


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

---

# ⚠ Disclaimer

This tool does not provide medical advice.
It is designed for personal behavioral tracking and experimentation.

---

# 📌 Status

Actively evolving.
Modular and extensible.
Built for long-term behavioral insight.
