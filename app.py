import streamlit as st

from model_service import LoanDefaultModel

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Loan Default Prediction",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# DESIGN SYSTEM
# Ink navy + muted gold, a serif headline against a clean sans
# body — a deliberate "underwriter's desk" feel rather than a
# generic SaaS dashboard.
# ============================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,300;9..144,400;9..144,500;9..144,600&family=Inter:wght@400;500;600;700&display=swap');

:root {
    --ink: #0B1B33;
    --ink-deep: #071426;
    --ink-soft: #33425C;
    --ink-faint: #7C879B;
    --paper: #F7F5F0;
    --panel: #FFFFFF;
    --line: #E4E0D6;
    --gold: #B08A2E;
    --gold-soft: #EFE4C8;
    --risk: #9A2B25;
    --risk-bg: #FBEAE8;
    --amber: #92650F;
    --amber-bg: #FBF2DF;
    --safe: #2F6D4F;
    --safe-bg: #E9F3EC;
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    color: var(--ink);
    font-variant-numeric: tabular-nums;
}

p, li, label {
    line-height: 1.55;
}

.stApp {
    background:
        radial-gradient(circle at 92% 4%, rgba(176,138,46,0.10), transparent 20rem),
        var(--paper);
}

[data-testid="stSidebar"],
section[data-testid="stSidebar"],
section[data-testid="stSidebar"] > div:first-child,
[data-testid="stSidebarContent"],
[data-testid="stSidebarUserContent"] {
    background: var(--ink) !important;
    border-right: none;
}
section[data-testid="stSidebar"] {
    border-right: 1px solid rgba(255,255,255,0.08);
    box-shadow: 12px 0 30px rgba(7,20,38,0.10);
}
section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
    color: #EDEFF3;
}
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] h4 {
    color: #FBFAF6 !important;
    font-family: 'Fraunces', serif;
    letter-spacing: 0.01em;
}
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] small,
section[data-testid="stSidebar"] label {
    color: #C8D0DD !important;
}
section[data-testid="stSidebar"] [data-testid="stCaptionContainer"] p {
    color: #AEB9C9 !important;
    line-height: 1.55;
}
section[data-testid="stSidebar"] hr {
    border-color: rgba(255,255,255,0.15);
}

.sidebar-brand {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 8px 0 22px;
    border-bottom: 1px solid rgba(255,255,255,0.12);
    margin-bottom: 22px;
}
.sidebar-mark {
    width: 38px;
    height: 38px;
    display: grid;
    place-items: center;
    background: var(--gold);
    color: var(--ink);
    font-family: 'Fraunces', serif;
    font-size: 22px;
    font-weight: 600;
    border-radius: 3px;
}
.sidebar-brand strong {
    display: block;
    color: #FBFAF6;
    font-family: 'Fraunces', serif;
    font-size: 18px;
    font-weight: 500;
}
.sidebar-brand span {
    display: block;
    color: #8996A9;
    font-size: 10px;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-top: 2px;
}
.sidebar-status {
    padding: 12px 13px;
    background: rgba(255,255,255,0.07);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 3px;
    margin: 18px 0 22px;
}
.sidebar-status-label {
    color: #8996A9;
    font-size: 10px;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 5px;
}
.sidebar-status-value {
    color: #F3D88C;
    font-size: 13px;
    font-weight: 600;
}
.sidebar-section-kicker {
    color: #8A6518 !important;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin: 4px 0 8px;
}

/* Keep the sidebar readable across Streamlit theme overrides. */
section[data-testid="stSidebar"],
section[data-testid="stSidebar"] > div,
section[data-testid="stSidebar"] [data-testid="stSidebarContent"],
section[data-testid="stSidebar"] [data-testid="stSidebarUserContent"] {
    background: #FFFDF8 !important;
    border-right-color: #E4E0D6 !important;
}
section[data-testid="stSidebar"] * {
    color: #0B1B33 !important;
}
section[data-testid="stSidebar"] .sidebar-brand span,
section[data-testid="stSidebar"] .sidebar-status-label,
section[data-testid="stSidebar"] [data-testid="stCaptionContainer"] p {
    color: #667085 !important;
}
section[data-testid="stSidebar"] .sidebar-mark {
    color: #071426 !important;
}
section[data-testid="stSidebar"] .sidebar-status-value {
    color: #8A6518 !important;
}
section[data-testid="stSidebar"] .sidebar-brand {
    border-bottom-color: #E4E0D6 !important;
}
section[data-testid="stSidebar"] .sidebar-status {
    background: #F3EFE5 !important;
    border-color: #DDD5C4 !important;
}
section[data-testid="stSidebar"] .model-name,
section[data-testid="stSidebar"] .model-score {
    color: #243550 !important;
}
section[data-testid="stSidebar"] .model-name.best::after {
    color: #0B1B33 !important;
}
section[data-testid="stSidebar"] .model-bar-track {
    background: #E4E0D6 !important;
}
section[data-testid="stSidebar"] .model-bar-fill {
    background: #9AA4B2 !important;
}
section[data-testid="stSidebar"] .model-bar-fill.best {
    background: #B08A2E !important;
}
section.stSidebar[data-testid="stSidebar"] > div[data-testid="stSidebarContent"] {
    background: #FFFDF8 !important;
    background-color: #FFFDF8 !important;
}
section.stSidebar[data-testid="stSidebar"] h3,
section.stSidebar[data-testid="stSidebar"] h4 {
    color: #0B1B33 !important;
}

/* Slightly larger type for comfortable reading. */
.stApp p,
.stApp li,
.stApp label {
    font-size: 15px;
}
label[data-testid="stWidgetLabel"] p {
    font-size: 14px !important;
}
.section-sub,
.empty-state,
.verdict p {
    font-size: 15px;
}
section[data-testid="stSidebar"] .model-name,
section[data-testid="stSidebar"] .model-score,
section[data-testid="stSidebar"] .sidebar-status-value {
    font-size: 14px !important;
}
section[data-testid="stSidebar"] [data-testid="stCaptionContainer"] p {
    font-size: 14px !important;
}

.block-container {
    padding-top: 2rem;
    max-width: 1100px;
}

/* ---------- Hero ---------- */
.hero {
    background: var(--ink);
    color: #F5F3EC;
    padding: 44px 48px;
    border-radius: 3px;
    box-shadow: 0 18px 34px rgba(11,27,51,0.12);
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: "";
    position: absolute;
    top: 0; left: 0; height: 4px; width: 100%;
    background: linear-gradient(90deg, var(--gold), transparent 70%);
}
.hero-eyebrow {
    color: var(--gold);
    font-size: 12px;
    letter-spacing: 0.08em;
    margin-bottom: 14px;
    font-weight: 600;
    text-transform: uppercase;
}
.hero h1 {
    font-family: 'Fraunces', serif;
    font-weight: 500;
    font-size: 42px;
    line-height: 1.2;
    letter-spacing: -0.01em;
    margin: 0 0 14px 0;
    color: #FBFAF6;
}
.hero p {
    color: #B7BFCE;
    font-size: 16px;
    line-height: 1.6;
    max-width: 540px;
    margin: 0;
}
.hero-stats {
    display: flex;
    flex-wrap: wrap;
    gap: 40px;
    margin-top: 30px;
    padding-top: 24px;
    border-top: 1px solid rgba(255,255,255,0.14);
}
.hero-stat-label {
    font-size: 11px;
    letter-spacing: 0.04em;
    color: #8B93A6;
    margin-bottom: 5px;
    text-transform: uppercase;
}
.hero-stat-value {
    font-family: 'Fraunces', serif;
    font-weight: 500;
    font-size: 23px;
    color: #FBFAF6;
}

/* ---------- Section labels ---------- */
.section-head {
    display: flex;
    align-items: baseline;
    gap: 10px;
    margin: 6px 0 2px 0;
}
.section-num {
    font-family: 'Fraunces', serif;
    font-size: 14px;
    color: var(--gold);
    font-weight: 600;
}
.section-label {
    font-family: 'Fraunces', serif;
    font-size: 23px;
    font-weight: 500;
    color: var(--ink);
    letter-spacing: -0.01em;
}
.section-sub {
    color: var(--ink-faint);
    font-size: 14px;
    margin-bottom: 16px;
}

/* ---------- Panel (native bordered container) ---------- */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background: var(--panel);
    border: 1px solid var(--line) !important;
    border-radius: 3px !important;
    box-shadow: 0 8px 22px rgba(11,27,51,0.04);
    margin-bottom: 22px;
}

/* Streamlit inputs */
label[data-testid="stWidgetLabel"] p {
    font-size: 15px !important;
    color: var(--ink-soft) !important;
    font-weight: 600 !important;
    letter-spacing: 0.01em;
}
div[data-baseweb="select"] > div, .stNumberInput input {
    border-radius: 2px !important;
    border-color: var(--line) !important;
    font-size: 16px !important;
    color: var(--ink) !important;
    font-weight: 500 !important;
}
div[data-baseweb="select"] span {
    font-size: 16px !important;
    color: var(--ink) !important;
}
div[data-baseweb="select"]:focus-within > div, .stNumberInput input:focus {
    border-color: var(--gold) !important;
    box-shadow: 0 0 0 1px var(--gold) !important;
}
[data-testid="stTooltipIcon"] {
    color: var(--ink-faint) !important;
}

/* Button */
div.stButton > button {
    background: var(--gold);
    color: var(--ink);
    border: none;
    border-radius: 3px;
    padding: 15px 0;
    font-weight: 600;
    font-size: 15px;
    letter-spacing: 0.02em;
    transition: background 0.15s ease, transform 0.1s ease;
}
div.stButton > button:hover,
div.stButton > button:focus,
div.stButton > button:focus-visible,
div.stButton > button:active {
    background: #D2AE55 !important;
    color: var(--ink-deep) !important;
    -webkit-text-fill-color: var(--ink-deep) !important;
    box-shadow: 0 8px 18px rgba(176,138,46,0.24);
}
div.stButton > button:active {
    transform: scale(0.99);
}

/* Empty state */
.empty-state {
    border: 1px dashed var(--line);
    padding: 28px;
    text-align: center;
    color: var(--ink-faint);
    font-size: 14px;
    margin-top: 22px;
}

/* Sidebar model comparison — custom, theme-matched (not st.dataframe) */
.model-row {
    margin-bottom: 8px;
    padding: 10px 11px;
    border: 1px solid transparent;
    border-radius: 3px;
    transition: background 0.15s ease, border-color 0.15s ease;
}
.model-row:hover {
    background: #F3EFE5;
    border-color: #DDD5C4;
}
.model-row:has(.model-name.best) {
    background: #F8F1DE;
    border-color: #E4D2A2;
}
.model-row-top {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    margin-bottom: 5px;
}
.model-name {
    font-size: 13px;
    font-weight: 600;
    color: #E7EAF0;
}
.model-name.best::after {
    content: "Selected";
    font-size: 9px;
    font-weight: 700;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    color: #0B1B33;
    background: var(--gold);
    padding: 2px 6px;
    border-radius: 2px;
    margin-left: 8px;
    vertical-align: middle;
    display: inline-block;
}
.model-score {
    font-family: 'Fraunces', serif;
    font-size: 13px;
    color: #B7BFCE;
}
.model-bar-track {
    height: 5px;
    border-radius: 3px;
    background: rgba(255,255,255,0.12);
    overflow: hidden;
}
.model-bar-fill {
    height: 100%;
    border-radius: 3px;
    background: rgba(255,255,255,0.4);
}
.model-bar-fill.best {
    background: var(--gold);
}
.risk-badge {
    display: inline-block;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    padding: 3px 9px;
    border-radius: 2px;
    margin-bottom: 10px;
}
.risk-badge.low { background: var(--safe-bg); color: var(--safe); }
.risk-badge.medium { background: var(--amber-bg); color: var(--amber); }
.risk-badge.high { background: var(--risk-bg); color: var(--risk); }

/* ---------- Result ---------- */
.verdict {
    padding: 24px 28px;
    border-left: 4px solid var(--risk);
    background: var(--risk-bg);
    margin-top: 6px;
    box-shadow: 0 10px 24px rgba(11,27,51,0.06);
}
.verdict.low { border-left-color: var(--safe); background: var(--safe-bg); }
.verdict.medium { border-left-color: var(--amber); background: var(--amber-bg); }
.verdict.high { border-left-color: var(--risk); background: var(--risk-bg); }
.verdict h3 {
    margin: 0 0 6px 0;
    font-family: 'Fraunces', serif;
    font-weight: 600;
    font-size: 21px;
    letter-spacing: -0.01em;
}
.verdict.low h3 { color: var(--safe); }
.verdict.medium h3 { color: var(--amber); }
.verdict.high h3 { color: var(--risk); }
.verdict p {
    margin: 0;
    color: var(--ink-soft);
    font-size: 14.5px;
    max-width: 560px;
}

/* Gauge */
.gauge-wrap {
    margin: 26px 4px 4px 4px;
}
.gauge-track {
    position: relative;
    height: 8px;
    border-radius: 6px;
    background: linear-gradient(90deg, var(--safe) 0%, var(--safe) 30%, #D9B23C 30%, #D9B23C 60%, var(--risk) 60%, var(--risk) 100%);
}
.gauge-marker {
    position: absolute;
    top: -6px;
    width: 3px;
    height: 20px;
    background: var(--ink);
    box-shadow: 0 0 0 3px rgba(11,27,51,0.12);
}
.gauge-labels {
    display: flex;
    justify-content: space-between;
    font-size: 12px;
    color: var(--ink-faint);
    margin-top: 10px;
}
.gauge-labels .current {
    color: var(--ink);
    font-weight: 600;
}

@media (max-width: 800px) {
    .block-container {
        padding: 1rem 1rem 2rem;
    }
    .hero {
        padding: 30px 24px;
    }
    .hero h1 {
        font-size: 34px;
    }
    .hero-stats {
        gap: 22px;
    }
    .section-label {
        font-size: 21px;
    }
}

footer, #MainMenu {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ============================================================
# LOAD TRAINED MODEL (train_model.py compares Logistic
# Regression, Random Forest, AdaBoost and Gradient Boosting,
# and saves the best one automatically)
# ============================================================

@st.cache_resource
def load_service():
    return LoanDefaultModel()

service = load_service()

# ============================================================
# HERO
# ============================================================

total_records = f"{len(service.data):,}" if service.data is not None else "N/A"

st.markdown(f"""
<div class="hero">
    <div class="hero-eyebrow">Loan Default Prediction</div>
    <h1>Will this applicant repay the loan?</h1>
    <p>Fill in an applicant's financial and personal details below to get an instant,
    data-backed default risk read — scored by the strongest of four models trained
    and compared on historical loan outcomes.</p>
    <div class="hero-stats">
        <div>
            <div class="hero-stat-label">Training records</div>
            <div class="hero-stat-value">{total_records}</div>
        </div>
        <div>
            <div class="hero-stat-label">Model in use</div>
            <div class="hero-stat-value">{service.best_model_name or 'N/A'}</div>
        </div>
        <div>
            <div class="hero-stat-label">Test accuracy</div>
            <div class="hero-stat-value">{service.metrics.get('accuracy', 0) * 100:.1f}%</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# SIDEBAR — model insights, kept out of the main flow
# ============================================================

with st.sidebar:
    st.markdown('''
    <div class="sidebar-brand">
        <div class="sidebar-mark">L</div>
        <div><strong>Loan Predictor</strong><span>Loan default prediction</span></div>
    </div>
    ''', unsafe_allow_html=True)
    st.markdown(f'''
    <div class="sidebar-status">
        <div class="sidebar-status-label">Model status</div>
        <div class="sidebar-status-value">● Ready · {service.best_model_name}</div>
    </div>
    ''', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-section-kicker">Models compared</div>', unsafe_allow_html=True)
    st.markdown("### Model results")
    st.caption(f"Selected automatically: **{service.best_model_name}** "
               f"(fit: {service.fit_verdict})")

    if service.comparison_table:
        rows = sorted(service.comparison_table, key=lambda r: r["test_score"], reverse=True)
        best_score = rows[0]["test_score"] if rows else 1

        rows_html = ""
        for r in rows:
            is_best = r["model"] == service.best_model_name
            fill_pct = (r["test_score"] / best_score) * 100 if best_score else 0
            rows_html += f"""
            <div class="model-row">
                <div class="model-row-top">
                    <span class="model-name{' best' if is_best else ''}">{r['model']}</span>
                    <span class="model-score">{r['test_score']*100:.1f}%</span>
                </div>
                <div class="model-bar-track">
                    <div class="model-bar-fill{' best' if is_best else ''}" style="width: {fill_pct:.0f}%;"></div>
                </div>
            </div>
            """

        st.markdown(rows_html, unsafe_allow_html=True)
        st.caption("Test accuracy across all 4 candidates — Logistic Regression, "
                   "Random Forest, AdaBoost, Gradient Boosting. "
                   "Retrain with `python train_model.py`.")
    else:
        st.write("Comparison table not available in this model bundle.")

    st.markdown("---")
    st.caption("Loan Default Prediction · Machine Learning Project")

# ============================================================
# LOAN APPLICATION FORM
# ============================================================

st.markdown(
    '<div class="section-head"><span class="section-num">01</span>'
    '<span class="section-label">Loan details</span></div>',
    unsafe_allow_html=True
)
st.markdown('<div class="section-sub">Income, credit and loan terms</div>', unsafe_allow_html=True)


def num_bounds(col, fallback_min, fallback_max, fallback_default):
    """Pull realistic min/max/default from the training data when available."""
    if service.data is not None and col in service.data.columns:
        series = service.data[col].dropna()
        lo = float(series.min())
        hi = float(series.max())
        default = float(service.defaults.get(col, series.median()))
        return lo, hi, default
    return fallback_min, fallback_max, service.defaults.get(col, fallback_default)


with st.container(border=True):
    col1, col2, col3 = st.columns(3)

    with col1:
        lo, hi, d = num_bounds("age", 18, 69, 30)
        age = st.number_input("Age", min_value=int(lo), max_value=int(hi), value=int(d),
                               help="Applicant's age in years.")

        lo, hi, d = num_bounds("income", 15000, 149999, 50000)
        income = st.number_input("Annual income", min_value=int(lo), max_value=int(hi), value=int(d),
                                  help="Gross yearly income before tax.")

        lo, hi, d = num_bounds("loanamount", 5000, 249999, 100000)
        loan_amount = st.number_input("Loan amount", min_value=int(lo), max_value=int(hi), value=int(d),
                                       help="Total amount being requested.")

    with col2:
        lo, hi, d = num_bounds("creditscore", 300, 849, 650)
        credit_score = st.number_input("Credit score", min_value=int(lo), max_value=int(hi), value=int(d),
                                        help="FICO-style score, typically 300–850. Higher is better.")

        lo, hi, d = num_bounds("monthsemployed", 0, 119, 24)
        months_employed = st.number_input("Months employed", min_value=int(lo), max_value=int(hi), value=int(d),
                                           help="Time at current job, in months.")

        lo, hi, d = num_bounds("numcreditlines", 1, 4, 2)
        num_credit_lines = st.number_input("Credit lines", min_value=int(lo), max_value=int(hi), value=int(d),
                                            help="Number of open credit accounts (cards, loans, etc.).")

    with col3:
        lo, hi, d = num_bounds("interestrate", 2.0, 25.0, 10.0)
        interest_rate = st.number_input("Interest rate (%)", min_value=float(lo), max_value=float(hi), value=float(d), step=0.01,
                                         help="Annual interest rate offered on this loan.")

        loan_term = st.selectbox("Loan term (months)", [12, 24, 36, 48, 60],
                                  help="Repayment period.")

        lo, hi, d = num_bounds("dtiratio", 0.10, 0.90, 0.50)
        dti_ratio = st.number_input("Debt-to-income ratio", min_value=float(lo), max_value=float(hi), value=float(d), step=0.01,
                                     help="Monthly debt payments divided by gross monthly income — lower is healthier.")

st.markdown(
    '<div class="section-head"><span class="section-num">02</span>'
    '<span class="section-label">Applicant details</span></div>',
    unsafe_allow_html=True
)
st.markdown('<div class="section-sub">Personal profile and reason for the loan</div>', unsafe_allow_html=True)

with st.container(border=True):
    col1, col2 = st.columns(2)

    with col1:
        education = st.selectbox("Education", service.options.get("education", ["High School", "Bachelor's", "Master's", "PhD"]))
        employment_type = st.selectbox("Employment type", service.options.get("employmenttype", ["Full-time", "Part-time", "Self-employed", "Unemployed"]))
        marital_status = st.selectbox("Marital status", service.options.get("maritalstatus", ["Single", "Married", "Divorced"]))
        loan_purpose = st.selectbox("Loan purpose", service.options.get("loanpurpose", ["Auto", "Business", "Education", "Home", "Other"]),
                                     help="What the applicant intends to use the loan for.")

    with col2:
        has_mortgage = st.selectbox("Has mortgage?", service.options.get("hasmortgage", ["Yes", "No"]))
        has_dependents = st.selectbox("Has dependents?", service.options.get("hasdependents", ["Yes", "No"]))
        has_cosigner = st.selectbox("Has co-signer?", service.options.get("hascosigner", ["Yes", "No"]),
                                     help="A co-signer shares responsibility for repayment.")

predict_button = st.button("Assess risk", use_container_width=True)

if not predict_button:
    st.markdown(
        '<div class="empty-state">Your risk assessment will appear here — '
        'fill in the form above and click <b>Assess risk</b>.</div>',
        unsafe_allow_html=True
    )

# ============================================================
# PREDICTION
# ============================================================

if predict_button:

    row = {
        "age": age,
        "income": income,
        "loanamount": loan_amount,
        "creditscore": credit_score,
        "monthsemployed": months_employed,
        "numcreditlines": num_credit_lines,
        "interestrate": interest_rate,
        "loanterm": loan_term,
        "dtiratio": dti_ratio,
        "education": education,
        "employmenttype": employment_type,
        "maritalstatus": marital_status,
        "hasmortgage": has_mortgage,
        "hasdependents": has_dependents,
        "loanpurpose": loan_purpose,
        "hascosigner": has_cosigner,
    }

    try:
        default_probability = service.predict_probability(row) * 100
    except Exception as e:
        st.error(f"Prediction failed: {e}")
        st.stop()

    st.markdown(
        '<div class="section-head"><span class="section-num">03</span>'
        '<span class="section-label">Prediction</span></div>',
        unsafe_allow_html=True
    )

    if default_probability < 30:
        tier = "low"
        badge = "Low risk"
        title = "Likely to repay"
        detail = (
            f"This applicant scores a {default_probability:.1f}% probability of default — "
            "well within a comfortable range. Standard underwriting terms should apply."
        )
    elif default_probability < 60:
        tier = "medium"
        badge = "Medium risk"
        title = "Borderline — worth a closer look"
        detail = (
            f"This applicant scores a {default_probability:.1f}% probability of default. "
            "Consider added conditions — a co-signer, a lower loan amount, or extra income verification."
        )
    else:
        tier = "high"
        badge = "High risk"
        title = "Likely to default"
        detail = (
            f"This applicant scores a {default_probability:.1f}% probability of default — "
            "meaningfully above a safe threshold. Recommend declining or restructuring the loan."
        )

    st.markdown(f"""
    <div class="verdict {tier}">
        <span class="risk-badge {tier}">{badge}</span>
        <h3>{title}</h3>
        <p>{detail}</p>
    </div>
    <div class="gauge-wrap">
        <div class="gauge-track">
            <div class="gauge-marker" style="left: calc({default_probability:.1f}% - 1.5px);"></div>
        </div>
        <div class="gauge-labels">
            <span>Low</span>
            <span class="current">{default_probability:.1f}% probability of default</span>
            <span>High</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.caption(f"Prediction made using the {service.best_model_name} model, "
               f"selected for the highest test accuracy among 4 candidates.")
