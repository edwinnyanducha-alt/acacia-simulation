# Belgo Strategic Simulation — Web App

**Kitisuru Corporate Campus — Decision Discovery Exercise**

A multi-group, multi-round strategic simulation for the Belgo Holdings board and family. Four groups compete under different archetypes (Stewards, Developers, Rainmakers, Gamblers) through 4 rounds of decisions — Ground Rules, Capital & Partners, The Shock, and Exit & Family.

Built with Streamlit. Live demo-ready.

## Quick Start

```bash
cd simulation_app
pip install -r requirements.txt
streamlit run app.py
```

Opens at `http://localhost:8501`.

## Deployment

### Streamlit Cloud (Free, Recommended)

1. Push this folder to a GitHub repository
2. Go to https://share.streamlit.io
3. Sign in with GitHub → "New app"
4. Select your repo, branch, set main file to `app.py`
5. Click Deploy

### Railway.app ($5-8/month)

```bash
railway login
railway init
railway up
```

## Project Structure

```
simulation_app/
├── app.py                  # Main application (entry point)
├── requirements.txt        # Python dependencies
├── .streamlit/             # Theme configuration
│   └── config.toml
└── engine/                 # Simulation engine
    ├── __init__.py
    ├── archetypes.py       # 4 archetypes with secrets
    ├── scoring.py          # Scoring engine (4 dimensions)
    └── implications.py     # Narrative implications (26 entries)
```

## Scoring Dimensions

| Dimension | Weight | Description |
|-----------|--------|-------------|
| Reputation | 25% | Public perception, stakeholder trust |
| IRR | 30% | Financial return on investment |
| Cash Velocity | 20% | Speed of cash generation |
| Resilience | 25% | Ability to withstand shocks |

## The Four Archetypes

| Group | Colour | Strategy |
|-------|--------|----------|
| **Stewards** | 🟢 Green | Patient, family-controlled, long-term value |
| **Developers** | 🔵 Blue | Aggressive, fast exit, value-maximising |
| **Rainmakers** | 🟡 Gold | Partnership-oriented, external capital |
| **Gamblers** | 🔴 Red | Speculative, maximum velocity |

---

*Confidential — Belgo Holdings Limited*
