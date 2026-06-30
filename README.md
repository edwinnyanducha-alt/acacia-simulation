# Acacia Strategic Simulation â€” Web App

**the Corporate Campus â€” Decision Discovery Exercise**

A multi-group, multi-round strategic simulation for the Acacia Holdings board and family. Four groups compete under different archetypes (Stewards, Developers, Rainmakers, Gamblers) through 4 rounds of decisions â€” Ground Rules, Capital & Partners, The Shock, and Exit & Family.

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
3. Sign in with GitHub â†’ "New app"
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
â”œâ”€â”€ app.py                  # Main application (entry point)
â”œâ”€â”€ requirements.txt        # Python dependencies
â”œâ”€â”€ .streamlit/             # Theme configuration
â”‚   â””â”€â”€ config.toml
â””â”€â”€ engine/                 # Simulation engine
    â”œâ”€â”€ __init__.py
    â”œâ”€â”€ archetypes.py       # 4 archetypes with secrets
    â”œâ”€â”€ scoring.py          # Scoring engine (4 dimensions)
    â””â”€â”€ implications.py     # Narrative implications (26 entries)
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
| **Stewards** | ðŸŸ¢ Green | Patient, family-controlled, long-term value |
| **Developers** | ðŸ”µ Blue | Aggressive, fast exit, value-maximising |
| **Rainmakers** | ðŸŸ¡ Gold | Partnership-oriented, external capital |
| **Gamblers** | ðŸ”´ Red | Speculative, maximum velocity |

---

*Confidential â€” Acacia Holdings Limited*
