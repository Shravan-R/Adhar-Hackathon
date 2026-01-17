import streamlit as st
from src.data_loader import load_all_datasets
from src.analysis import biometric_age_trend

st.set_page_config(
    page_title="Aadhaar Analytics Dashboard",
    layout="wide"
)

st.title("Aadhaar Analytics Dashboard")

# ---------------- EXECUTIVE SUMMARY ---------------- #

st.markdown("## Executive Summary")

st.write("""
This dashboard provides a decision-support view of Aadhaar enrolment and
biometric update activity using official, aggregated datasets.

The analysis focuses on identifying societal patterns, operational anomalies,
and regional disparities to support informed planning and service optimization.
""")

st.markdown("""
**Key Capabilities:**
- Monitor biometric update behavior across age groups
- Track enrolment trends over time and across states
- Detect unusual spikes or drops in update activity
- Enable state-level drill-down for targeted analysis
""")

st.markdown("""
**Policy Value:**
- Supports infrastructure planning and resource allocation
- Helps identify regions requiring outreach or audits
- Encourages data-driven governance while maintaining privacy
""")

st.caption("Decision Support System for Enrolment & Update Trends")

with st.spinner("Loading datasets..."):
    enrolment_df, biometric_df, demographic_df = load_all_datasets()

st.success("Data loaded successfully")

col1, col2, col3 = st.columns(3)
col1.metric("Enrolment Records", f"{len(enrolment_df):,}")
col2.metric("Biometric Records", f"{len(biometric_df):,}")
col3.metric("Demographic Records", f"{len(demographic_df):,}")

st.markdown("---")
st.header("Biometric Update Trends by Age Group")

trend_df = biometric_age_trend(biometric_df)
st.line_chart(trend_df.set_index("date"))

st.info(
    "Insight: Biometric update activity varies across age groups, "
    "reflecting lifecycle-related biometric changes and access needs."
)

st.success(
    "Recommendation: Plan update infrastructure and outreach programs "
    "based on age-specific biometric demand trends."
)


# ---------------- STATE FILTER ---------------- #

st.markdown("### State Filter")

all_states = sorted(
    set(biometric_df["state"].dropna().unique())
)

selected_state = st.selectbox(
    "Select State",
    options=["All States"] + all_states
)

if selected_state != "All States":
    biometric_filtered = biometric_df[biometric_df["state"] == selected_state]
    enrolment_filtered = enrolment_df[enrolment_df["state"] == selected_state]
else:
    biometric_filtered = biometric_df
    enrolment_filtered = enrolment_df


# ---------------- ENROLMENT ANALYSIS ---------------- #

from src.analysis import enrolment_time_trend, enrolment_by_state

st.markdown("---")
st.header("Aadhaar Enrolment Trends")

# Time trend
enrol_trend = enrolment_time_trend(enrolment_df)
st.subheader("Enrolment Trend Over Time")
st.line_chart(enrol_trend.set_index("date"))

# State-wise
st.subheader("Top States by Enrolment Volume")
state_enrol = enrolment_by_state(enrolment_df)
st.bar_chart(state_enrol.set_index("state").head(10))

st.info(
    "Insight: Enrolment growth trends indicate varying levels of Aadhaar saturation "
    "across states, with some regions showing stable maturity while others continue "
    "to record high enrolment activity."
)

st.success(
    "Recommendation: Redirect enrolment infrastructure and outreach efforts "
    "towards regions with sustained enrolment growth, while shifting mature regions "
    "towards update and maintenance-focused services."
)


# ---------------- ANOMALY DETECTION ---------------- #

from src.analysis import biometric_anomaly_detection

st.markdown("---")
st.header("Anomaly Monitoring: Biometric Updates")

daily_updates, anomalies = biometric_anomaly_detection(biometric_df)

st.subheader("Daily Biometric Update Volume")
st.line_chart(
    daily_updates.set_index("date")[["total_updates"]]
)

if not anomalies.empty:
    st.warning(
        f"⚠️ {len(anomalies)} anomalous days detected with unusually high or low update activity."
    )
    st.dataframe(
        anomalies[["date", "total_updates", "z_score"]]
        .sort_values("z_score", ascending=False)
    )
else:
    st.success("No significant anomalies detected in biometric update activity.")

st.info(
    "Insight: Sudden spikes or drops in biometric updates may indicate "
    "operational disruptions, special enrollment drives, or regional system issues."
)

st.success(
    "Recommendation: Flag anomalous periods for administrative review and "
    "temporarily reinforce infrastructure or outreach where required."
)


#----- DATA & PRIVACYNOTE------#
st.markdown("---")
st.caption(
    "Data Note: This dashboard uses aggregated, anonymized Aadhaar-related datasets "
    "provided for analytical purposes only. No personally identifiable information (PII) "
    "is stored, processed, or displayed. The system is designed following privacy-by-design "
    "and data minimization principles."
)


#------------Limitations------#

st.markdown("### Limitations")

st.write("""
- The analysis is based on historical, aggregated datasets and does not reflect real-time updates.
- Regional variations may be influenced by reporting frequency and data completeness.
- Anomaly detection is statistical and should be supplemented with administrative validation.
""")



