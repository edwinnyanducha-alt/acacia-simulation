import streamlit as st
import random
import datetime
import pandas as pd
import plotly.graph_objects as go
from typing import Dict, Optional

# Page config must be first
st.set_page_config(
    page_title="Acacia Strategic Simulation",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# â”€â”€ Imports â”€â”€
from engine.archetypes import ARCHETYPES, get_archetype_by_colour
from engine.scoring import calculate_scores
from engine.implications import IMPLICATIONS, build_implications_from_decisions

# â”€â”€ Styling â”€â”€
st.markdown("""
<style>
    /* ── Base font stack ── */
    html, body, .stApp, .stMarkdown, p, div, span, li, label {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif !important;
    }
    
    /* ── Global ── */
    .stApp { background-color: #1B2C3D; }
    .stButton > button { 
        border-radius: 8px; 
        font-weight: 600; 
        font-size: 1rem;
        letter-spacing: 0.3px;
    }
    
    /* ── Cards ── */
    .decision-card {
        background: #2C3E50;
        border: 1px solid #3D5166;
        border-radius: 12px;
        padding: 1.2rem;
        margin-bottom: 0.8rem;
    }
    .card-selected {
        border: 2px solid #009688 !important;
        background: #1A3A35 !important;
    }
    .card-header { 
        color: #D4A017; 
        font-weight: 700; 
        font-size: 1.1rem; 
        margin-bottom: 0.5rem;
        letter-spacing: 0.5px;
    }
    .card-subtitle { 
        color: #BDC3C7; 
        font-size: 0.9rem; 
        margin-bottom: 0.3rem; 
    }
    
    /* ── Envelope reveal ── */
    .envelope {
        background: linear-gradient(135deg, #2C3E50, #1B2C3D);
        border: 2px solid #D4A017;
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
        animation: pulse 2s infinite;
    }
    @keyframes pulse { 0% {transform: scale(1);} 50% {transform: scale(1.02);} 100% {transform: scale(1);} }
    
    /* ── Shock card ── */
    .shock-card {
        background: linear-gradient(135deg, #4A0E0E, #C0392B);
        border: 2px solid #E74C3C;
        border-radius: 12px;
        padding: 1.5rem;
        color: white;
    }
    .shock-title { 
        font-size: 1.5rem; 
        font-weight: 700; 
        text-transform: uppercase; 
        letter-spacing: 2px;
        color: #FFD700;
    }
    .shock-text { 
        font-style: italic; 
        font-size: 1rem; 
        line-height: 1.6; 
        color: #F0F0F0;
    }
    
    /* ── Scoreboard ── */
    .scoreboard { border-collapse: collapse; width: 100%; }
    .scoreboard th { background: #1B2C3D; color: #D4A017; padding: 8px; text-align: center; }
    .scoreboard td { padding: 8px; text-align: center; border-bottom: 1px solid #3D5166; }
    .score-highlight { color: #D4A017; font-weight: 700; }
    .score-negative { color: #E74C3C; }
    
    /* ── Status badges ── */
    .badge-green { background: #27AE60; color: white; padding: 3px 12px; border-radius: 12px; font-size: 0.85rem; font-weight: 600; }
    .badge-gold { background: #D4A017; color: #1B2C3D; padding: 3px 12px; border-radius: 12px; font-size: 0.85rem; font-weight: 600; }
    .badge-red { background: #C0392B; color: white; padding: 3px 12px; border-radius: 12px; font-size: 0.85rem; font-weight: 600; }
    .badge-gray { background: #7F8C8D; color: white; padding: 3px 12px; border-radius: 12px; font-size: 0.85rem; font-weight: 600; }
    
    /* ── Round indicator ── */
    .round-indicator { display: inline-block; width: 50px; height: 50px; border-radius: 50%; 
                       text-align: center; line-height: 50px; font-weight: 700; margin: 0 10px; }
    
    /* ── Section divider ── */
    .section-divider { border: none; height: 2px; background: linear-gradient(90deg, #009688, #D4A017, #009688); margin: 2rem 0; }
    
    /* ── Facilitator-only watermark ── */
    .facilitator-badge {
        background: #C0392B; color: white; 
        padding: 4px 16px; border-radius: 20px;
        font-weight: 600; font-size: 0.85rem;
        display: inline-block; position: absolute; top: 10px; right: 10px;
        letter-spacing: 1px;
    }
    
    /* ── All radio button labels ── */
    .stRadio label, .stSelectbox label {
        font-size: 1rem !important;
    }
    .stRadio div[role="radiogroup"] label p {
        font-size: 0.95rem !important;
    }
    
    /* ── Mobile responsive ── */
    @media (max-width: 768px) {
        .decision-card { padding: 0.8rem; }
        .stButton > button { font-size: 0.9rem; }
    }
</style>
""", unsafe_allow_html=True)


# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# SESSION STATE INIT
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•

def init_state():
    """Initialise all session state variables."""
    defaults = {
        'page': 'landing',
        'role': None,  # 'facilitator' or 'group'
        'group_colour': None,
        'archetype': None,
        'session_code': None,
        'session_created': False,
        'current_round': 0,
        'round_locked': [False, False, False, False, False],  # 0-indexed, index 0 = R1
        'round_submitted': [False, False, False, False, False],
        'decisions': {},
        'scores': None,
        'secret_revealed': False,
        'secret_acknowledged': False,
        'shock_assigned': False,
        'shock_index': 0,
        'shock_responded': False,
        'facilitator_reveal_phase': 0,  # 0=none, 1=scores, 2=secrets, 3=ideals, 4=implications
        'session_archived': False,
        'all_groups_connected': {'Stewards': False, 'Developers': False, 'Rainmakers': False, 'Gamblers': False},
        'all_groups_submitted': {'Stewards': False, 'Developers': False, 'Rainmakers': False, 'Gamblers': False},
        'group_decisions': {},  # facilitator collects all groups' decisions
        'group_scores': {},     # facilitator collects all groups' scores
        'session_started': False,
        'show_hidden_scores': False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


init_state()

# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# UTILITY COMPONENTS
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•

def card_button(key: str, label: str, value, options: list,
                group_col: Optional[str] = None, help_text: str = "") -> bool:
    """Render a selectable card button, returns True if clicked."""
    cols = st.columns(len(options))
    current = st.session_state.get(key, options[0])
    clicked = False
    
    for i, opt in enumerate(options):
        is_selected = (current == opt)
        border = "#009688" if is_selected else "#3D5166"
        bg = "#1A3A35" if is_selected else "#2C3E50"
        
        with cols[i]:
            label_text = label.format(opt) if '{' in label else f"{label}: {opt}"
            display = f"{'[OK] ' if is_selected else ''}{opt}"
            if help_text:
                display += f"\n{help_text}"
            
            if st.button(display, key=f"{key}_{opt}", use_container_width=True,
                         type="primary" if is_selected else "secondary"):
                st.session_state[key] = opt
                return True
    return False


def archetype_card(colour: str, name: str, desc: str, hex_col: str) -> None:
    """Render an archetype info card."""
    st.markdown(
        f"""
        <div style="background:{hex_col}22; border:1px solid {hex_col}; border-radius:12px; padding:1rem; margin-bottom:0.5rem;">
            <span style="color:{hex_col}; font-weight:700; font-size:1.2rem;">[*] {name}</span>
            <p style="color:#ECF0F1; font-size:0.85rem; margin-top:0.3rem;">{desc}</p>
        </div>
        """,
        unsafe_allow_html=True
    )


def round_header(round_num: int, title: str, colour: str = "#D4A017") -> None:
    """Render a round header."""
    st.markdown(
        f"""
        <div style="margin-bottom:0.5rem;">
            <div style="display:flex; align-items:center; gap:1rem;">
                <div style="background:{colour}; color:#1B2C3D; width:50px; height:50px; border-radius:50%; 
                            display:flex; align-items:center; justify-content:center; font-weight:800; font-size:1.2rem;">
                    R{round_num}
                </div>
                <div>
                    <div style="color:{colour}; font-weight:700; font-size:1.4rem;">{title}</div>
                </div>
            </div>
        </div>
        <hr class="section-divider">
        """,
        unsafe_allow_html=True
    )


def status_badge(text: str, status: str) -> str:
    """Return HTML for a status badge."""
    colours = {
        'success': 'badge-green',
        'warning': 'badge-gold',
        'danger': 'badge-red',
        'neutral': 'badge-gray',
    }
    cls = colours.get(status, 'badge-gray')
    return f'<span class="{cls}">{text}</span>'


# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# PAGE ROUTER
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•

def landing_page():
    """Landing page  -  facilitator or group entry."""
    st.markdown(
        """
        <div style="text-align:center; padding: 4rem 2rem 2rem 2rem;">
            <div style="font-size:3rem; margin-bottom:1rem;">🏢</div>
            <h1 style="color:#ECF0F1; font-size:2.5rem; margin-bottom:0.5rem;">Acacia Strategic Simulation</h1>
            <p style="color:#D4A017; font-size:1.3rem; font-style:italic; margin-bottom:2rem;">
                the Corporate Campus &mdash; Decision Discovery Exercise
            </p>
            <hr class="section-divider">
        </div>
        """,
        unsafe_allow_html=True
    )
    
    col1, col2, col3 = st.columns([1, 4, 1])
    with col2:
        col_a, col_b = st.columns(2)
        
        with col_a:
            if st.button("  >>  Start New Session", use_container_width=True, type="primary"):
                st.session_state.role = 'facilitator'
                st.session_state.page = 'facilitator_setup'
                st.rerun()
        
        with col_b:
            if st.button("  <>  Join Session", use_container_width=True, type="secondary"):
                st.session_state.role = 'group'
                st.session_state.page = 'group_join'
                st.rerun()
        
        st.markdown(
            """
            <div style="text-align:center; margin-top:3rem; padding:1.5rem; background:#2C3E50; border-radius:12px; border:1px solid #3D5166;">
                <p style="color:#7F8C8D; font-size:0.9rem;">
                    <b>Session Code:</b> <span style="color:#D4A017; font-size:1.3rem; letter-spacing:8px;">_ _ _ _</span>
                    &nbsp;&nbsp;|&nbsp;&nbsp; 
                    <b>Table:</b> <span style="display:inline-block; width:16px; height:16px; border-radius:50%; background:#27AE60;"></span>
                    <span style="display:inline-block; width:16px; height:16px; border-radius:50%; background:#2980B9;"></span>
                    <span style="display:inline-block; width:16px; height:16px; border-radius:50%; background:#D4A017;"></span>
                    <span style="display:inline-block; width:16px; height:16px; border-radius:50%; background:#C0392B;"></span>
                </p>
                <p style="color:#7F8C8D; font-size:0.8rem; margin-top:0.5rem;">
                    CONFIDENTIAL &mdash; Acacia Holdings Limited
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )


def facilitator_setup():
    """Facilitator creates a new session."""
    col1, col2, col3 = st.columns([1, 3, 1])
    with col1:
        if st.button("[BACK] Back", use_container_width=True):
            st.session_state.page = 'landing'
            st.session_state.role = None
            st.rerun()
    
    with col2:
        st.markdown(
            '<div style="text-align:center; padding:1rem 0;">'
            '<h2 style="color:#ECF0F1;">  [>>] New Session</h2>'
            '<p style="color:#7F8C8D;">Create a simulation session and share the code with participants.</p>'
            '</div>',
            unsafe_allow_html=True
        )
        
        title = st.text_input("Session Title", value=f"Acacia Simulation  -  {datetime.date.today().strftime('%d %b %Y')}")
        num_groups = st.selectbox("Number of Groups", [4, 3], index=0)
        
        if not st.session_state.session_created:
            if st.button("Generate Session Code", type="primary", use_container_width=True):
                code = str(random.randint(1000, 9999))
                st.session_state.session_code = code
                st.session_state.session_created = True
                st.session_state.page = 'facilitator_dashboard'
                st.session_state.current_round = 1
                st.rerun()
        
        st.markdown(
            '<p style="color:#7F8C8D; font-size:0.85rem; margin-top:1rem;">'
            '<b>Note:</b> 4-digit session code is the only access control. '
            'Share it with participants. No accounts needed.</p>',
            unsafe_allow_html=True
        )


def group_join():
    """Group participant joins by entering session code and choosing colour."""
    col1, col2, col3 = st.columns([1, 3, 1])
    with col1:
        if st.button("[BACK] Back", use_container_width=True):
            st.session_state.page = 'landing'
            st.session_state.role = None
            st.rerun()
    
    with col2:
        st.markdown(
            '<div style="text-align:center; padding:1rem 0;">'
            '<h2 style="color:#ECF0F1;">  <> Join Simulation</h2>'
            '</div>',
            unsafe_allow_html=True
        )
        
        # Simulated session code entry
        code_digits = []
        code_str = st.text_input("Session Code (4 digits)", max_chars=4, placeholder="e.g. 7429",
                                  help="Enter the 4-digit code displayed by the facilitator.")
        
        if code_str:
            st.markdown(f'<p style="color:#27AE60;">Session <b>{code_str}</b> found.</p>',
                        unsafe_allow_html=True)
            
            st.markdown("<h3 style='color:#D4A017; margin-top:1rem;'>Choose Your Table</h3>", unsafe_allow_html=True)
            col_a, col_b = st.columns(2)
            col_c, col_d = st.columns(2)
            
            with col_a:
                if st.button("  (G)  Green (Stewards)\nPatient. Guardian. Long-term.", use_container_width=True):
                    st.session_state.group_colour = "Green"
                    st.session_state.archetype = ARCHETYPES["Stewards"]
                    st.session_state.page = 'group_round'
                    st.session_state.current_round = 1
                    st.rerun()
            
            with col_b:
                if st.button("  (B)  Blue (Developers)\nAggressive. Value-maximiser.", use_container_width=True):
                    st.session_state.group_colour = "Blue"
                    st.session_state.archetype = ARCHETYPES["Developers"]
                    st.session_state.page = 'group_round'
                    st.session_state.current_round = 1
                    st.rerun()
            
            with col_c:
                if st.button("  (Y)  Gold (Rainmakers)\nConnected. Partnership-seeker.", use_container_width=True):
                    st.session_state.group_colour = "Gold"
                    st.session_state.archetype = ARCHETYPES["Rainmakers"]
                    st.session_state.page = 'group_round'
                    st.session_state.current_round = 1
                    st.rerun()
            
            with col_d:
                if st.button("  (R)  Red (Gamblers)\nBold. Speed-obsessed.", use_container_width=True):
                    st.session_state.group_colour = "Red"
                    st.session_state.archetype = ARCHETYPES["Gamblers"]
                    st.session_state.page = 'group_round'
                    st.session_state.current_round = 1
                    st.rerun()


def group_input_round(round_num: int):
    """Generic group input screen for any round."""
    if not st.session_state.archetype:
        st.error("Please join a session first.")
        if st.button("Go to Join Page"):
            st.session_state.page = 'group_join'
            st.rerun()
        return
    
    arch = st.session_state.archetype
    hex_col = arch.hex_colour
    
    # Top bar
    col_a, col_b, col_c = st.columns([2, 1, 1])
    with col_a:
        st.markdown(
            f'<span style="color:{hex_col}; font-weight:700;">[*] {arch.name}</span> '
            f'<span style="color:#7F8C8D;">| Session: {st.session_state.session_code or "----"}</span>',
            unsafe_allow_html=True
        )
    with col_b:
        if st.session_state.round_submitted[round_num - 1]:
            st.markdown(f'<span class="badge-green">[OK] Round {round_num} Submitted</span>',
                        unsafe_allow_html=True)
        else:
            st.markdown(f'<span class="badge-gold">Round {round_num}  -  Awaiting Input</span>',
                        unsafe_allow_html=True)
    with col_c:
        if st.button("[END] End Session", type="secondary"):
            st.session_state.page = 'landing'
            st.session_state.role = None
            st.rerun()
    
    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
    
    if round_num == 1:
        round_header(1, "Ground Rules", hex_col)
        group_round1(arch)
    elif round_num == 2:
        round_header(2, "Capital & Partners", hex_col)
        group_round2(arch)
    elif round_num == 3:
        round_header(3, "The Shock", hex_col)
        group_round3(arch)
    elif round_num == 4:
        round_header(4, "Exit & Family", hex_col)
        group_round4(arch)


def group_round1(arch):
    """Round 1  -  Ground Rules decision cards."""
    col1, col2 = st.columns([3, 2])
    
    with col1:
        # Q1: NDA
        st.markdown('<div class="decision-card"><div class="card-header">Q1: Net Developable Acres</div>'
                    '<div class="card-subtitle">How many of the 65 net acres do you develop?</div>',
                    unsafe_allow_html=True)
        nda = st.radio("NDA", [55, 60, 65], index=[55, 60, 65].index(st.session_state.get('decisions', {}).get('nda', 55)),
                       format_func=lambda x: f"{x} acres{'   [P] (premium)' if x==55 else ' [B]     (balanced)' if x==60 else '   [R] (max revenue)'}",
                       horizontal=True, key="r1_nda", label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Q2: Green Space
        st.markdown('<div class="decision-card"><div class="card-header">Q2: Green Space</div>'
                    '<div class="card-subtitle">What % of developed land remains as green/open space?</div>',
                    unsafe_allow_html=True)
        green = st.radio("Green Space", [40, 30, 20, 10],
                         index=[40, 30, 20, 10].index(st.session_state.get('decisions', {}).get('green_space', 40)),
                         format_func=lambda x: f"{x}% {'  [$]  [$]  [$]  [$] (premium)' if x==40 else '  [$]  [$]  [$] (standard)' if x==30 else '  [$]  [$] (minimum)' if x==20 else '  [$] (bare)'}",
                         horizontal=True, key="r1_green", label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Q3: Monetisation archetype
        st.markdown('<div class="decision-card"><div class="card-header">Q3: Monetisation Approach</div>'
                    '<div class="card-subtitle">How do you convert land to cash?</div>',
                    unsafe_allow_html=True)
        mon_options = ["Steward", "Balanced", "Developer", "Speculator"]
        mon_labels = {
            "Steward": "[S] Steward  -  70% lease / 20% JV / 10% sale",
            "Balanced": "[B]     Balanced  -  40% lease / 30% JV / 30% sale",
            "Developer": " [D] Developer  -  20% lease / 20% JV / 60% sale",
            "Speculator": "[R] Speculator  -  10% lease / 20% JV / 70% sale",
        }
        mon = st.radio("Monetisation", mon_options,
                       index=mon_options.index(st.session_state.get('decisions', {}).get('monetisation', 'Balanced')),
                       format_func=lambda x: mon_labels[x],
                       horizontal=False, key="r1_mon", label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Q4: Infrastructure
        st.markdown('<div class="decision-card"><div class="card-header">Q4: Infrastructure Timing</div>', unsafe_allow_html=True)
        infra = st.radio("Infrastructure", ["Just-in-time", "Phased", "Full upfront"],
                         index=["Just-in-time", "Phased", "Full upfront"].index(
                             st.session_state.get('decisions', {}).get('infra', 'Phased')),
                         format_func=lambda x: f"{'  [JIT] ' if x=='Just-in-time' else '  [P] ' if x=='Phased' else '      —       '}{x}",
                         horizontal=True, key="r1_infra", label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        # Q5-7: Relationships
        st.markdown('<div class="decision-card"><div class="card-header">Q5-7: Stakeholder Relationships</div>'
                    '<div class="card-subtitle">Budget: KES 30M total (10M per Strategic relationship)</div>',
                    unsafe_allow_html=True)
        
        rel_options = {0: "  [x] Ignore (KES 0M)", 1: "  [i] Admin (KES 5M)", 2: "  [$] Strategic (KES 10M)"}
        
        nbo = st.selectbox("      ¢ NBO (Neighbouring Business Organisation)",
                           [0, 1, 2], format_func=lambda x: rel_options[x],
                           key="r1_nbo",
                           index=st.session_state.get('decisions', {}).get('nbo_r1', 2))
        gov = st.selectbox("      ›       GOV (County Government)",
                           [0, 1, 2], format_func=lambda x: rel_options[x],
                           key="r1_gov",
                           index=st.session_state.get('decisions', {}).get('gov_r1', 2))
        fin = st.selectbox("      ¦ FIN (Financial Institutions)",
                           [0, 1, 2], format_func=lambda x: rel_options[x],
                           key="r1_fin",
                           index=st.session_state.get('decisions', {}).get('fin_r1', 1))
        
        budget = (nbo + gov + fin) * 5  # million
        remaining = 30 - budget
        st.markdown(
            f'<div style="margin-top:0.5rem; padding:0.5rem; background:#1B2C3D; border-radius:8px;">'
            f'<b>Budget:</b> KES {budget}M / 30M  '
            f'<span style="color:{"#27AE60" if remaining>=0 else "#E74C3C"};">'
            f'({"KES " + str(remaining) + "M remaining" if remaining>=0 else "OVER BUDGET!"})</span>'
            f'</div>',
            unsafe_allow_html=True
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Secret preview
        st.markdown(
            '<div style="text-align:center; padding:1rem; background:#2C3E50; border-radius:12px; border:1px dashed #D4A017; margin-top:1rem;">'
            '<p style="color:#D4A017; font-size:0.9rem;">  [*] Secret information will be revealed after Round 1 is locked.</p>'
            '</div>',
            unsafe_allow_html=True
        )
    
    # Submit button
    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("[>>] Submit Round 1", type="primary", use_container_width=True, disabled=False):
            # Save decisions
            st.session_state.decisions['nda'] = nda
            st.session_state.decisions['green_space'] = green
            st.session_state.decisions['monetisation'] = mon
            st.session_state.decisions['infra'] = infra
            st.session_state.decisions['nbo_r1'] = nbo
            st.session_state.decisions['gov_r1'] = gov
            st.session_state.decisions['fin_r1'] = fin
            
            st.session_state.round_submitted[0] = True
            st.session_state.secret_revealed = True
            st.rerun()


def secret_reveal_screen():
    """Show the secret envelope after Round 1 is submitted."""
    arch = st.session_state.archetype
    hex_col = arch.hex_colour
    
    st.markdown(f"""
    <div style="text-align:center; padding:3rem;">
        <div style="font-size:4rem;">🏢</div>
        <h2 style="color:#D4A017; margin:1rem 0;">Your Group Has Received a Sealed Message</h2>
        <p style="color:#7F8C8D; font-size:1.1rem;">Read it silently. Do not reveal to other groups.</p>
    </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.secret_acknowledged:
        if st.button("[OPEN] Open Your Envelope", type="primary", use_container_width=True):
            st.session_state.secret_acknowledged = True
            st.rerun()
    else:
        st.markdown(f"""
        <div style="max-width:700px; margin:2rem auto; background: #F5E6D0; border-radius:16px; padding:2.5rem;
                    border:2px solid #D4A017; box-shadow: 0 8px 32px rgba(0,0,0,0.3);">
            <div style="text-align:center; margin-bottom:1.5rem;">
                <span style="background:{hex_col}; color:white; padding:4px 16px; border-radius:20px; font-size:0.9rem;">
                    [*] {arch.name}
                </span>
            </div>
            <div style="color:#2C3E50; font-size:1rem; line-height:1.6;">
                <p style="margin-bottom:1rem;"><b>Your win condition:</b> {arch.win_condition}</p>
                <hr style="border:1px dashed #D4A017; margin:1rem 0;">
                <p style="font-style:italic;">{arch.secret_text}</p>
            </div>
            <div style="text-align:center; margin-top:1.5rem;">
                <span style="background:{hex_col}22; color:{hex_col}; padding:4px 12px; border-radius:8px; font-size:0.8rem;">
                    This is your private information. Do not share with other groups.
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("[OK] I Acknowledge", type="primary", use_container_width=True):
            st.session_state.current_round = 2
            st.rerun()


def group_round2(arch):
    """Round 2  -  Capital & Partners."""
    col1, col2 = st.columns([3, 2])
    
    with col1:
        # Q1: Debt/Equity
        st.markdown('<div class="decision-card"><div class="card-header">Q1: Debt / Equity Split</div>', unsafe_allow_html=True)
        debt = st.slider("Debt %", 0, 100, st.session_state.get('decisions', {}).get('debt_pct', 40), 10, key="r2_debt")
        st.markdown(f'<p style="color:#95A5A6;">Equity: {100-debt}%  |  Debt: {debt}%  |  '
                    f'<span style="color:{"#E74C3C" if debt>70 else "#27AE60" if debt<30 else "#F1C40F"}">'
                    f'{"[!] Aggressive" if debt>70 else "[OK] Conservative" if debt<30 else "Standard"}</span></p>',
                    unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Q2: External Partner
        st.markdown('<div class="decision-card"><div class="card-header">Q2: External Partner</div>', unsafe_allow_html=True)
        partner = st.radio("Partner", ["None", "Minority (30%)", "JV (50%)", "Majority (70%+)"],
                           index=["None", "Minority (30%)", "JV (50%)", "Majority (70%+)"].index(
                               st.session_state.get('decisions', {}).get('partner_type', 'None')),
                           horizontal=True, key="r2_partner", label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Q3: Developer Quality
        st.markdown('<div class="decision-card"><div class="card-header">Q3: Developer Quality</div>', unsafe_allow_html=True)
        dev = st.radio("Developer", ["Premium", "Mid-tier", "Lowest bid"],
                       index=["Premium", "Mid-tier", "Lowest bid"].index(
                           st.session_state.get('decisions', {}).get('dev_quality', 'Mid-tier')),
                       horizontal=True, key="r2_dev", label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        # Q4-6: Relationships
        st.markdown('<div class="decision-card"><div class="card-header">Q4-6: Stakeholder Relationships</div>'
                    '<div class="card-subtitle">Round 2  -  Budget: KES 30M</div>',
                    unsafe_allow_html=True)
        rel_options = {0: "  [x] Ignore", 1: "  [i] Admin", 2: "  [$] Strategic"}
        nbo = st.selectbox("NBO", [0, 1, 2], format_func=lambda x: rel_options[x],
                           key="r2_nbo", index=1)
        gov = st.selectbox("GOV", [0, 1, 2], format_func=lambda x: rel_options[x],
                           key="r2_gov", index=1)
        fin = st.selectbox("FIN", [0, 1, 2], format_func=lambda x: rel_options[x],
                           key="r2_fin", index=1)
        budget = (nbo + gov + fin) * 5
        st.markdown(f'<p style="color:#95A5A6;">Budget: KES {budget}M / 30M</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Private information reminder
        st.markdown(
            f'<div style="padding:1rem; background:#D4A01722; border-radius:12px; border:1px dotted #D4A017; margin-top:1rem;">'
            f'<p style="color:#D4A017; font-size:0.85rem;"><b>  [*] Your Private Information</b></p>'
            f'<p style="color:#ECF0F1; font-size:0.85rem;"><i>{arch.secret_text[:120]}...</i></p>'
            f'</div>',
            unsafe_allow_html=True
        )
    
    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("[>>] Submit Round 2", type="primary", use_container_width=True):
            decisions = st.session_state.decisions
            decisions['debt_pct'] = debt
            decisions['partner_type'] = partner.replace(" (30%)", "").replace(" (50%)", "").replace(" (70%+)", "")
            decisions['dev_quality'] = dev
            decisions['nbo_r2'] = nbo
            decisions['gov_r2'] = gov
            decisions['fin_r2'] = fin
            st.session_state.round_submitted[1] = True
            st.session_state.current_round = 3
            st.rerun()


def group_round3(arch):
    """Round 3  -  The Shock."""
    if not st.session_state.shock_assigned:
        # Assign random shock
        shock_idx = random.randint(0, 3)
        st.session_state.shock_index = shock_idx
        st.session_state.shock_assigned = True
    
    shocks = [
        ("THE RIVAL", "Tatu City Expansion",
         "Tatu City announces a KES 15B expansion targeting the same corporate tenants you're negotiating with. "
         "They offer SEZ tax breaks that you can't match  -  unless you get your own SEZ designation."),
        ("PARTNER DEFAULT", "Equity Partner Default",
         "Your external equity partner defaults on their capital commitment. KES 400M is now unavailable. "
         "Without it, Phase 1 construction stops."),
        ("COURT CASE", "Residents' Injunction",
         "A Residents' Association files an injunction against your development. They claim your environmental "
         "impact assessment was inadequate. Court hearing in 60 days. Your project is paused."),
        ("REGULATORY REVERSAL", "County Planning Review",
         "The County Government announces a review of all development approvals in the. A new planning "
         "directive reduces maximum building heights by 40%. Your approved plans need revision."),
    ]
    
    shock_title, shock_subtitle, shock_text = shocks[st.session_state.shock_index]
    
    # Shock card display
    st.markdown(f"""
    <div class="shock-card">
        <div class="shock-title">[!] {shock_title}</div>
        <div style="font-size:1.1rem; margin-bottom:1rem;">{shock_subtitle}</div>
        <hr style="border-color:#E74C3C44;">
        <div class="shock-text">"{shock_text}"</div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        # Response
        st.markdown('<div class="decision-card"><div class="card-header">Your Response</div>', unsafe_allow_html=True)
        pivot = st.radio("Response",
                         [("  [JIT] PIVOT", 2), ("  [$] NEGOTIATE", 1), ("[X] FIGHT", 0)],
                         format_func=lambda x: x[0],
                         horizontal=True, key="r3_pivot", label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        # Emergency relationships
        st.markdown('<div class="decision-card"><div class="card-header">Emergency Relationships</div>'
                    '<div class="card-subtitle">Budget: KES 15M</div>', unsafe_allow_html=True)
        rel_opts = {0: "Ignore", 1: "Inform", 2: "Strategic"}
        nbo = st.selectbox("NBO (emergency)", [0, 1, 2], format_func=lambda x: rel_opts[x], key="r3_nbo", index=1)
        gov = st.selectbox("GOV (emergency)", [0, 1, 2], format_func=lambda x: rel_opts[x], key="r3_gov", index=1)
        fin = st.selectbox("FIN (emergency)", [0, 1, 2], format_func=lambda x: rel_opts[x], key="r3_fin", index=1)
        budget = (nbo + gov + fin) * 5
        st.markdown(f'<p style="color:#95A5A6;">Budget: KES {budget}M / 15M</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("[>>] Submit Round 3", type="primary", use_container_width=True):
            decisions = st.session_state.decisions
            decisions['pivot'] = pivot[1]
            decisions['nbo_r3'] = nbo
            decisions['gov_r3'] = gov
            decisions['fin_r3'] = fin
            st.session_state.round_submitted[2] = True
            st.session_state.current_round = 4
            st.rerun()


def group_round4(arch):
    """Round 4  -  Exit & Family."""
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown(
            '<div style="text-align:center; padding:1.5rem; background:#1B2C3D; border-radius:12px; border:2px solid #D4A017; margin-bottom:1rem;">'
            '<h3 style="color:#D4A017;">Unsolicited Offer: KES 88 Billion ($1.1B)</h3>'
            '<p style="color:#7F8C8D;">A consortium offers KES 1B/acre for the entire 88 acres.</p>'
            '</div>',
            unsafe_allow_html=True
        )
        
        # Q1: Offer
        st.markdown('<div class="decision-card"><div class="card-header">Q1: Response to Offer</div>', unsafe_allow_html=True)
        offer = st.radio("Offer", [0, 1, 2, 3],
                         format_func=lambda x: ["  [OK] Accept  -  Sell everything (KES 88B)",
                                                 "  [$] Counter  -  Propose 60/40 JV",
                                                 "  [x]       Decline  -  Land is not for sale",
                                                 "  [JV] Counter with partner"][x],
                         horizontal=False, key="r4_offer", label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Q2: Dispute
        st.markdown('<div class="decision-card"><div class="card-header">Q2: Dispute Resolution</div>'
                    '<div class="card-subtitle">A family member challenges your decision.</div>',
                    unsafe_allow_html=True)
        dispute = st.radio("Dispute", [0, 1, 2, 3],
                           format_func=lambda x: ["  [VOTE]       Family vote  -  Let democracy decide",
                                                   "  [$] Mediation  -  Independent mediator",
                                                   "  [BUY] Buy-out  -  Purchase dissent share",
                                                   "[B]     Court  -  Let courts decide"][x],
                           horizontal=False, key="r4_dispute", label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        # Q3: Constitution
        st.markdown('<div class="decision-card"><div class="card-header">Q3: Family Constitution</div>',
                    unsafe_allow_html=True)
        constitution = st.radio("Constitution", [1, 0],
                                format_func=lambda x: "[OK] Yes  -  Lock governance rules" if x else "[X] No  -  Deal with it later",
                                horizontal=True, key="r4_constitution", label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Q4: Legacy Statement
        st.markdown('<div class="decision-card"><div class="card-header">Q4: Legacy Statement</div>'
                    '<div class="card-subtitle">In 2060, Acacia should be known for...</div>',
                    unsafe_allow_html=True)
        legacy = st.text_area("Legacy", placeholder="What do you want Acacia to be remembered for in 2060?",
                              key="r4_legacy", label_visibility="collapsed", height=100)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Q5-7: Final Relationships
        st.markdown('<div class="decision-card"><div class="card-header">Q5-7: Final Relationships</div>', unsafe_allow_html=True)
        rel_opts = {0: "Ignore", 1: "Admin", 2: "Strategic"}
        nbo = st.selectbox("NBO", [0, 1, 2], format_func=lambda x: rel_opts[x], key="r4_nbo", index=1)
        gov = st.selectbox("GOV", [0, 1, 2], format_func=lambda x: rel_opts[x], key="r4_gov", index=1)
        fin = st.selectbox("FIN", [0, 1, 2], format_func=lambda x: rel_opts[x], key="r4_fin", index=1)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("[>>] Submit Final Round", type="primary", use_container_width=True):
            decisions = st.session_state.decisions
            decisions['offer'] = offer
            decisions['dispute'] = dispute
            decisions['constitution'] = constitution
            decisions['legacy'] = legacy
            decisions['nbo_r4'] = nbo
            decisions['gov_r4'] = gov
            decisions['fin_r4'] = fin
            decisions['secret_acknowledged'] = st.session_state.secret_acknowledged
            
            st.session_state.round_submitted[3] = True
            st.session_state.current_round = 5  # results
            st.rerun()


def group_results():
    """Show results to the group."""
    decisions = st.session_state.decisions
    scores = calculate_scores(decisions)
    arch = st.session_state.archetype
    
    st.markdown(
        '<div style="text-align:center; padding:1.5rem;">'
        '<h1 style="color:#D4A017;"> [*] Your Results</h1>'
        '<p style="color:#7F8C8D;">Waiting for the facilitator to reveal final scores...</p>'
        '</div>',
        unsafe_allow_html=True
    )
    
    # Sneak preview of their own scores
    col1, col2, col3, col4 = st.columns(4)
    metrics = [("Reputation", scores['reputation'], 25),
               ("IRR", scores['irr'], 30),
               ("Cash Velocity", scores['velocity'], 20),
               ("Resilience", scores['resilience'], 25)]
    for col, (label, val, weight) in zip([col1, col2, col3, col4], metrics):
        with col:
            colour = "#27AE60" if val >= 80 else "#F1C40F" if val >= 50 else "#E74C3C"
            st.markdown(
                f'<div style="text-align:center; padding:1rem; background:#2C3E50; border-radius:12px; border:1px solid {colour};">'
                f'<p style="color:#7F8C8D; font-size:0.8rem;">{label} ({weight}%)</p>'
                f'<p style="color:{colour}; font-size:2rem; font-weight:700;">{val}</p>'
                f'</div>',
                unsafe_allow_html=True
            )
    
    # Weighted total
    st.markdown(
        f'<div style="text-align:center; padding:1rem; margin-top:1rem; background:#1B2C3D; border-radius:12px; border:2px solid #D4A017;">'
        f'<p style="color:#7F8C8D;">Weighted Total</p>'
        f'<p style="color:#D4A017; font-size:2.5rem; font-weight:700;">{scores["weighted_total"]:.1f}</p>'
        f'<p style="color:#7F8C8D; font-size:0.85rem;">Your group archetype: <b>{arch.name}</b></p>'
        f'</div>',
        unsafe_allow_html=True
    )
    
    # Implications
    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
    st.markdown('<h3 style="color:#D4A017;">  [*] Your Decision Implications</h3>', unsafe_allow_html=True)
    
    implications = build_implications_from_decisions(decisions)
    for label, text in implications:
        with st.expander(f"  [*] {label}"):
            st.markdown(f'<p style="color:#ECF0F1; line-height:1.6;">{text}</p>', unsafe_allow_html=True)


def facilitator_dashboard():
    """Facilitator's command centre."""
    st.markdown(
        '<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:1rem;">'
        '<h2 style="color:#ECF0F1; margin:0;">  [>>] Facilitator Dashboard</h2>'
        f'<div><span class="badge-red">FACILITATOR ONLY</span> '
        f'<span style="color:#D4A017; font-weight:700; margin-left:1rem;">Code: {st.session_state.session_code or "----"}</span></div>'
        '</div>',
        unsafe_allow_html=True
    )
    
    # Session info bar
    col_a, col_b, col_c, col_d = st.columns(4)
    with col_a:
        st.markdown(f'<p style="color:#27AE60;">[*] Stewards</p>', unsafe_allow_html=True)
    with col_b:
        st.markdown(f'<p style="color:#2980B9;">[*] Developers</p>', unsafe_allow_html=True)
    with col_c:
        st.markdown(f'<p style="color:#D4A017;">[*] Rainmakers</p>', unsafe_allow_html=True)
    with col_d:
        st.markdown(f'<p style="color:#C0392B;">[*] Gamblers</p>', unsafe_allow_html=True)
    
    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
    
    # Round progression
    col_rounds = st.columns(4)
    round_names = ["R1: Ground Rules", "R2: Capital", "R3: Shock", "R4: Exit"]
    for i, (col, name) in enumerate(zip(col_rounds, round_names)):
        with col:
            status = "success" if st.session_state.round_submitted[i] else ("warning" if st.session_state.current_round >= i+1 else "neutral")
            label = "[OK] Done" if st.session_state.round_submitted[i] else ("[>>] Active" if st.session_state.current_round == i+1 else "[...] Waiting")
            st.markdown(f'<div style="text-align:center; padding:0.5rem; background:#2C3E50; border-radius:8px;">'
                        f'<p style="color:{("#27AE60" if status=="success" else "#D4A017" if status=="warning" else "#7F8C8D")};">{name}</p>'
                        f'<span class="badge-{status}">{label}</span></div>',
                        unsafe_allow_html=True)
    
    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
    
    # Simulated group status
    st.markdown('<h3 style="color:#ECF0F1;">Group Submission Status</h3>', unsafe_allow_html=True)
    status_data = [
        ["Stewards", "  (G)", "[OK]", "Connected"],
        ["Developers", "  (B)", "[OK]", "Connected"],
        ["Rainmakers", "  (Y)", "[>>]", "Connected"],
        ["Gamblers", "  (R)", "[--]", "Not yet joined"],
    ]
    st.table(pd.DataFrame(status_data, columns=["Group", "Colour", "Round 1", "Status"]))
    
    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
    
    # Hidden scoreboard
    col_hide, col_reveal = st.columns([1, 1])
    with col_hide:
        hidden = st.toggle("  [..] Hidden Scores (toggle to show)", value=st.session_state.show_hidden_scores)
        st.session_state.show_hidden_scores = hidden
    
    if st.session_state.show_hidden_scores:
        # Demo scores
        demo_scores = {
            "Stewards": {"Rep": 130, "IRR": 80, "Vel": 45, "Res": 105, "Total": 91.8},
            "Developers": {"Rep": 10, "IRR": 40, "Vel": 55, "Res": 55, "Total": 39.2},
            "Rainmakers": {"Rep": 120, "IRR": 90, "Vel": 50, "Res": 95, "Total": 90.8},
            "Gamblers": {"Rep": 10, "IRR": 30, "Vel": 80, "Res": -10, "Total": 25.0},
        }
        
        st.markdown(
            '<div style="padding:1rem; background:#1B2C3D; border-radius:12px; border:1px solid #E74C3C;">'
            '<p style="color:#E74C3C; font-weight:700;">  [*] REAL-TIME SCORES (Hidden from Groups)</p>',
            unsafe_allow_html=True
        )
        
        df = pd.DataFrame(demo_scores).T
        st.dataframe(df, use_container_width=True)
        
        # Radar chart
        categories = ['Reputation', 'IRR', 'Cash Velocity', 'Resilience']
        fig = go.Figure()
        colours = {'Stewards': '#27AE60', 'Developers': '#2980B9', 'Rainmakers': '#D4A017', 'Gamblers': '#C0392B'}
        for group, color in colours.items():
            vals = demo_scores[group]
            fig.add_trace(go.Scatterpolar(
                r=[vals['Rep'], vals['IRR'], vals['Vel'], vals['Res']],
                theta=categories,
                fill='toself',
                name=group,
                line_color=color,
            ))
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 150])),
            showlegend=True,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='#ECF0F1',
            height=400,
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
    
    # Reveal sequence
    st.markdown('<h3 style="color:#D4A017;">Reveal Sequence</h3>', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    phases = [
        ("1: Show Scores", 'facilitator_reveal_phase', 1, col1),
        ("2: Show Secrets", 'facilitator_reveal_phase', 2, col2),
        ("3: Show Ideals", 'facilitator_reveal_phase', 3, col3),
        ("4: Implications", 'facilitator_reveal_phase', 4, col4),
    ]
    
    for label, key, val, col in phases:
        with col:
            phase = st.session_state.facilitator_reveal_phase
            if st.button(label, use_container_width=True,
                         type="primary" if phase >= val else "secondary",
                         disabled=(phase < val - 1)):
                st.session_state.facilitator_reveal_phase = val
                st.rerun()
    
    # Show what's been revealed
    if st.session_state.facilitator_reveal_phase >= 1:
        st.markdown('<div style="padding:1rem; background:#2C3E50; border-radius:12px; margin-top:1rem; border:1px solid #27AE60;">'
                    '<h4 style="color:#27AE60;">[OK] Scores Revealed</h4>'
                    '<p style="color:#7F8C8D;">The scoreboard is being projected to the room.</p></div>',
                    unsafe_allow_html=True)
    
    if st.session_state.facilitator_reveal_phase >= 2:
        st.markdown('<div style="padding:1rem; background:#2C3E50; border-radius:12px; margin-top:1rem; border:1px solid #D4A017;">'
                    '<h4 style="color:#D4A017;">[OK] Secrets Revealed</h4>'
                    '<p style="color:#7F8C8D;">Each group\'s secret mission is now visible to the room.</p></div>',
                    unsafe_allow_html=True)
    
    if st.session_state.facilitator_reveal_phase >= 3:
        st.markdown('<div style="padding:1rem; background:#2C3E50; border-radius:12px; margin-top:1rem; border:1px solid #2980B9;">'
                    '<h4 style="color:#2980B9;">[OK] Ideal Responses Shown</h4>'
                    '<p style="color:#7F8C8D;">Per-archetype optimal choices displayed for comparison.</p></div>',
                    unsafe_allow_html=True)
    
    if st.session_state.facilitator_reveal_phase >= 4:
        st.markdown('<div style="padding:1rem; background:#2C3E50; border-radius:12px; margin-top:1rem; border:1px solid #27AE60;">'
                    '<h4 style="color:#27AE60;">[OK] Implications Displayed</h4>'
                    '<p style="color:#7F8C8D;">Full implications library accessible. Discussion prompts active.</p></div>',
                    unsafe_allow_html=True)
    
    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
    
    # Archive
    col_arc1, col_arc2 = st.columns(2)
    with col_arc1:
        if st.button("  [+] Archive Session", use_container_width=True, type="primary"):
            st.session_state.session_archived = True
            st.success("Session archived to SQLite. PDF summary ready for download.")
    with col_arc2:
        if st.button("[END] End Session", use_container_width=True, type="secondary"):
            for k in list(st.session_state.keys()):
                del st.session_state[k]
            st.rerun()


# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# MAIN ROUTER
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•

def main():
    """Route to the correct page based on state."""
    page = st.session_state.get('page', 'landing')
    role = st.session_state.get('role')
    
    if page == 'landing':
        landing_page()
    elif page == 'facilitator_setup':
        facilitator_setup()
    elif page == 'group_join':
        group_join()
    elif page == 'facilitator_dashboard':
        facilitator_dashboard()
    elif page == 'group_round':
        round_num = st.session_state.get('current_round', 1)
        if round_num == 1 and st.session_state.get('round_submitted', [False]*4)[0]:
            # After R1 submit, show secret envelope always until current_round advances to 2
            # secret_reveal_screen handles both [OPEN] and [OK] I Acknowledge internally
            secret_reveal_screen()
        else:
            group_input_round(round_num)
        if round_num >= 5:
            group_results()
    else:
        landing_page()


if __name__ == "__main__":
    main()
