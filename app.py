import streamlit as st
from datetime import date
from dateutil.relativedelta import relativedelta
from dateutil import parser
import streamlit.components.v1 as components

# --- PAGE SETUP ---
st.set_page_config(page_title="Disc Follow-Up Calculator", layout="centered")
st.title("📅 Disc Follow-Up Date Calculator")

# --- STATE RULES ---
THREE_YEAR_STATES = {
    "AK","AR","CA","CO","DE","FL","GA","ID","IL","KS",
    "LA","MN","MS","MT","NJ","NM","NY","OK","PA",
    "SC","TN","UT","VA","WV","NV",
}
TWO_YEAR_STATES = {"DC","WY","RI","CT"}

STATE_FULL_NAMES = {
    "AK": "Alaska","AR": "Arkansas","CA": "California","CO": "Colorado",
    "DE": "Delaware","FL": "Florida","GA": "Georgia","ID": "Idaho",
    "IL": "Illinois","KS": "Kansas","KY": "Kentucky","LA": "Louisiana",
    "MN": "Minnesota","MS": "Mississippi","MT": "Montana","ND": "North Dakota",
    "NJ": "New Jersey","NM": "New Mexico","NY": "New York","OK": "Oklahoma",
    "PA": "Pennsylvania","SC": "South Carolina","TN": "Tennessee",
    "UT": "Utah","VA": "Virginia","WV": "West Virginia","DC": "District of Columbia",
    "WY": "Wyoming","RI": "Rhode Island","CT": "Connecticut","NV": "Nevada",
}

# Reverse mapping for dropdown
state_abbr_map = {full: abbr for abbr, full in STATE_FULL_NAMES.items()}

# --- DATE INPUTS (FLEXIBLE) ---
completion_date_str = st.text_input(
    "Certificate Completion Date (M/D/Y)",
    value=date.today().strftime("%m/%d/%Y")
)

policy_expiration_str = st.text_input(
    "Next Policy Renewal Date (M/D/Y)",
    value=date.today().strftime("%m/%d/%Y")
)

# --- DATE PARSING FUNCTION ---
def parse_us_date(date_str):
    """Parse a US-style date string and return a date object or None if invalid."""
    try:
        return parser.parse(date_str, dayfirst=False).date()
    except Exception:
        return None

completion_date = parse_us_date(completion_date_str)
policy_expiration = parse_us_date(policy_expiration_str)

# Validation flag
dates_valid = True

if not completion_date:
    st.error("Please enter a valid completion date (e.g., 1/2/2026)")
    dates_valid = False

if not policy_expiration:
    st.error("Please enter a valid policy renewal date (e.g., 1/2/2026)")
    dates_valid = False

# --- STATE SELECTION (ALWAYS VISIBLE) ---
state_full = st.selectbox(
    "State",
    sorted(STATE_FULL_NAMES.values())
)
state = state_abbr_map[state_full]

nd_age = None
if state == "ND":
    nd_age = st.radio("ND Age Group", ["Under 55", "55 or older"])

# --- CALCULATIONS (ONLY IF DATES ARE VALID) ---
if dates_valid:
    # Determine certificate validity
    if state in THREE_YEAR_STATES:
        years_valid = 3
    elif state in TWO_YEAR_STATES:
        years_valid = 2
    elif state == "KY":
        years_valid = 5
    elif state == "ND":
        years_valid = 2 if nd_age == "Under 55" else 3
    else:
        years_valid = 3

    # Certificate expiration
    certificate_expiration = completion_date + relativedelta(years=years_valid)

    # Next policy renewal after expiration
    policy_month = policy_expiration.month
    policy_day = policy_expiration.day
    next_renewal = date(certificate_expiration.year, policy_month, policy_day)
    if next_renewal <= certificate_expiration:
        next_renewal = date(certificate_expiration.year + 1, policy_month, policy_day)

    # Disc follow-up date
    disc_follow_up_date = next_renewal - relativedelta(months=3)

    # --- DISPLAY RESULTS ---
    st.markdown(
        f"""
        Please follow-up for a new accident prevention course certificate.
        The current certificate expires **{certificate_expiration.strftime('%m/%d/%Y')}**.<br><br>

        <span style='color:green; font-weight:bold; font-size:30px;'>
            Disc Follow-Up Date: {disc_follow_up_date.strftime('%m/%d/%Y')}
        </span>
        """,
        unsafe_allow_html=True
    )

    # --- COPY BUTTON ---
    copy_text = (
        f"Please follow-up for a new accident prevention course certificate. "
        f"The current certificate expires {certificate_expiration.strftime('%m/%d/%Y')}."
    )

    components.html(f"""
    <textarea id="msg" style="display:none;">{copy_text}</textarea>
    <button onclick="
    var copyText = document.getElementById('msg');
    copyText.style.display='block';
    copyText.select();
    document.execCommand('copy');
    copyText.style.display='none';
    alert('Message copied to clipboard!');
    ">📋 Copy Message</button>
    """, height=60)





























