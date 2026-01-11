import streamlit as st
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from dateutil.parser import parse
import streamlit.components.v1 as components

# --- Helper function for flexible date parsing ---
def parse_flexible_date(input_str):
    """Parse dates like 1/1/2025, 01/01/2025, 1/25/2025."""
    try:
        parsed_date = parse(input_str, dayfirst=False).date()
        return parsed_date
    except Exception:
        return None

# --- Page setup ---
st.set_page_config(page_title="Disc Follow-Up Calculator", layout="centered")
st.title("📅 Disc Follow-Up Date Calculator")

# --- State expiration rules ---
THREE_YEAR_STATES = {"AK","AR","CA","CO","DE","FL","GA","ID","IL","KS",
                     "LA","MN","MS","MT","NJ","NM","NY","OK","PA",
                     "SC","TN","UT","VA","WV"}
TWO_YEAR_STATES = {"DC","WY","RI"}

STATE_FULL_NAMES = {
    "AK": "Alaska","AR": "Arkansas","CA": "California","CO": "Colorado",
    "DE": "Delaware","FL": "Florida","GA": "Georgia","ID": "Idaho",
    "IL": "Illinois","KS": "Kansas","KY": "Kentucky","LA": "Louisiana",
    "MN": "Minnesota","MS": "Mississippi","MT": "Montana","ND": "North Dakota",
    "NJ": "New Jersey","NM": "New Mexico","NY": "New York","OK": "Oklahoma",
    "PA": "Pennsylvania","SC": "South Carolina","TN": "Tennessee",
    "UT": "Utah","VA": "Virginia","WV": "West Virginia","DC": "District of Columbia",
    "WY": "Wyoming","RI": "Rhode Island"
}

state_abbr_map = {full: abbr for abbr, full in STATE_FULL_NAMES.items()}

# --- Flexible Date Inputs with validation ---
completion_input = st.text_input("Certificate Completion Date (e.g., 1/1/2025)")
policy_input = st.text_input("Next Policy Renewal Date (e.g., 1/1/2025)")

completion_date = parse_flexible_date(completion_input) if completion_input else None
policy_expiration = parse_flexible_date(policy_input) if policy_input else None

# Show real-time error messages if dates are invalid
if completion_input and not completion_date:
    st.error("❌ Invalid Completion Date. Please use MM/DD/YYYY or similar.")
if policy_input and not policy_expiration:
    st.error("❌ Invalid Policy Renewal Date. Please use MM/DD/YYYY or similar.")

# Only proceed if both dates are valid
if completion_date and policy_expiration:
    # --- State selection ---
    state_full = st.selectbox("State", sorted(STATE_FULL_NAMES.values()))
    state = state_abbr_map[state_full]

    nd_age = None
    if state == "ND":
        nd_age = st.radio("ND Age Group", ["Under 55", "55 or older"])

    # --- Determine certificate expiration in years ---
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

    # --- Calculate Certificate Expiration ---
    certificate_expiration = completion_date + relativedelta(years=years_valid)

    # --- Calculate Next Policy Renewal AFTER Certificate Expiration ---
    policy_month = policy_expiration.month
    policy_day = policy_expiration.day

    next_renewal = date(certificate_expiration.year, policy_month, policy_day)
    if next_renewal <= certificate_expiration:
        next_renewal = date(certificate_expiration.year + 1, policy_month, policy_day)

    disc_follow_up_date = next_renewal - relativedelta(months=3)

    # --- Display Message ---
    st.markdown(
        f"✅ Please follow-up for a new accident prevention course certificate. "
        f"The current certificate expires **{certificate_expiration.strftime('%m/%d/%Y')}**.<br><br>"
        f"<span style='color:green;'>Disc Follow-Up Date: {disc_follow_up_date.strftime('%m/%d/%Y')}</span>",
        unsafe_allow_html=True
    )

    # --- Copy Button ---
    copy_text = f"Please follow-up for a new accident prevention course certificate. The current certificate expires {certificate_expiration.strftime('%m/%d/%Y')}."
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














