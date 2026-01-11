from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import streamlit as st
import streamlit.components.v1 as components

# --- Page setup ---
st.set_page_config(page_title="Disc Follow-Up Calculator", layout="centered")
st.title("📅 Disc Follow-Up Date Calculator")

# --- User Inputs as text ---
def parse_date(input_str):
    """Try to parse date in M/D/YYYY or MM/DD/YYYY format."""
    try:
        return datetime.strptime(input_str, "%m/%d/%Y").date()
    except ValueError:
        try:
            return datetime.strptime(input_str, "%-m/%-d/%Y").date()  # works on Linux/macOS
        except ValueError:
            st.error("Invalid date format! Use M/D/YYYY or MM/DD/YYYY.")
            return None

completion_str = st.text_input("Certificate Completion Date", value=date.today().strftime("%-m/%-d/%Y"))
policy_str = st.text_input("Policy Expiration Date", value=date.today().strftime("%-m/%-d/%Y"))

completion_date = parse_date(completion_str)
policy_expiration = parse_date(policy_str)

if completion_date and policy_expiration:
    # --- Dropdown with states ---
    STATE_FULL_NAMES = {"AK": "Alaska","AR": "Arkansas","CA": "California"}  # truncated for brevity
    state_abbr_map = {full: abbr for abbr, full in STATE_FULL_NAMES.items()}
    state_full = st.selectbox("State", sorted(STATE_FULL_NAMES.values()))
    state = state_abbr_map[state_full]

    # Example: simple 3-year rule
    years_valid = 3
    certificate_expiration = completion_date + relativedelta(years=years_valid)
    next_renewal = date(certificate_expiration.year, policy_expiration.month, policy_expiration.day)
    if next_renewal <= certificate_expiration:
        next_renewal = date(certificate_expiration.year + 1, policy_expiration.month, policy_expiration.day)
    disc_follow_up_date = next_renewal - relativedelta(months=3)

    st.markdown(
        f"Certificate expires {certificate_expiration.strftime('%m/%d/%Y')}<br>"
        f"Disc Follow-Up Date: {disc_follow_up_date.strftime('%m/%d/%Y')}",
        unsafe_allow_html=True
    )








