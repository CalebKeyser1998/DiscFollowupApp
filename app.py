import streamlit as st
from datetime import date
from dateutil.relativedelta import relativedelta
import streamlit.components.v1 as components

# Page setup
st.set_page_config(page_title="Disc Follow-Up Calculator", layout="centered")
st.title("📅 Disc Follow-Up Date Calculator")

# State expiration rules
THREE_YEAR_STATES = {
    "AK","AR","CA","CO","DE","FL","GA","ID","IL","KS",
    "LA","MN","MS","MT","NJ","NM","NY","OK","PA",
    "SC","TN","UT","VA","WV"
}
TWO_YEAR_STATES = {"DC","WY","RI"}

# Mapping of state abbreviations to full names
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

# Create a reverse mapping for dropdown selection
state_abbr_map = {full: abbr for abbr, full in STATE_FULL_NAMES.items()}

# User Inputs (MM/DD/YYYY)
completion_date = st.date_input(
    "Certificate Completion Date",
    value=date.today(),
    format="MM/DD/YYYY"
)

policy_expiration = st.date_input(
    "Next Policy Renewal Date",
    value=date.today(),
    format="MM/DD/YYYY"
)

# Dropdown with full state names
state_full = st.selectbox(
    "State",
    sorted(STATE_FULL_NAMES.values())
)
state = state_abbr_map[state_full]  # Convert back to abbreviation for calculations

nd_age = None
if state == "ND":
    nd_age = st.radio("ND Age Group", ["Under 55", "55 or older"])

# Determine certificate expiration in years
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

# Calculate Certificate Expiration
certificate_expiration = completion_date + relativedelta(years=years_valid)

# Calculate Next Policy Renewal AFTER Certificate Expiration
policy_month = policy_expiration.month
policy_day = policy_expiration.day

next_renewal = date(certificate_expiration.year, policy_month, policy_day)
if next_renewal <= certificate_expiration:
    next_renewal = date(certificate_expiration.year + 1, policy_month, policy_day)

disc_follow_up_date = next_renewal - relativedelta(months=3)

# Display Message 
st.markdown(
    f"Please follow-up for a new accident prevention course certificate. The current certificate expires {certificate_expiration.strftime('%m/%d/%Y')}.<br><br>"
    f"<span style='color:green;'>Disc Follow-Up Date: {disc_follow_up_date.strftime('%m/%d/%Y')}</span>",
    unsafe_allow_html=True
)

# Copy Button 
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








