"""Hiring Stall Alerter — a transparent, AI-assisted build with human review."""

from datetime import date
from pathlib import Path

import pandas as pd
import streamlit as st

from engine import assess_candidates, read_candidates, summarize
from csv_export import export_followups_csv

ROOT = Path(__file__).resolve().parent
SAMPLE = ROOT / "sample_hiring_board.csv"
SAMPLE_REFERENCE_DATE = date(2026, 11, 17)  # date the fictional sample data was built for


def show_table(df: pd.DataFrame) -> None:
    """Full-width table that works across Streamlit versions.

    `use_container_width` is deprecated in newer Streamlit releases in favor of
    `width="stretch"`; older releases only understand the former.
    """
    try:
        st.dataframe(df, hide_index=True, width="stretch")
    except Exception:
        st.dataframe(df, hide_index=True, use_container_width=True)


st.set_page_config(page_title="Hiring Stall Alerter", page_icon="⏳", layout="wide")

st.title("⏳ Hiring Stall Alerter")
st.write(
    "Upload a hiring-board CSV, spot candidates who haven't progressed, "
    "and get a prioritized list of follow-up actions."
)
st.caption("Demo tool · No messages are sent · No AI API key required · Dates and priorities follow visible rules")

st.subheader("1. Choose hiring-board data")
source = st.radio("Data source", ["Try example data", "Upload a CSV"], horizontal=True)

default_date = SAMPLE_REFERENCE_DATE if source == "Try example data" else date.today()

with st.sidebar:
    st.header("Detection settings")
    analysis_date = st.date_input(
        "Analyze as of",
        value=default_date,
        help="The example data opens on its reference date (2026-11-17). Uploaded files default to today.",
    )
    threshold = st.slider("Flag after this many days", min_value=1, max_value=30, value=7)
    st.info("Only active stages are checked. Hired, Rejected, Withdrawn, Closed, Declined and Not selected are excluded.")
    with st.expander("How priority works"):
        st.write(
            "**Urgent**: 7+ days beyond your limit, or a candidate in Offer/Final Interview "
            "3+ days beyond. **High**: 3+ days beyond, or Offer/Final Interview at the limit. "
            "**Follow up**: all other flagged candidates. Within each level, candidates "
            "are ranked by days overdue, then by hiring stage."
        )

if source == "Try example data":
    raw_data = SAMPLE.read_bytes()
    st.caption("This is fictional sample data generated for the challenge; reference date: 2026-11-17.")
else:
    uploaded = st.file_uploader("Upload a UTF-8 CSV", type=["csv"], accept_multiple_files=False)
    if uploaded is None:
        st.info("Select a CSV to start. Download the sample template below if you need a starting point.")
        st.download_button("Download sample CSV", SAMPLE.read_bytes(), file_name="sample_hiring_board.csv", mime="text/csv")
        st.stop()
    raw_data = uploaded.getvalue()

with st.expander("Required CSV columns and sample template"):
    st.code("candidate_id,candidate_name,role,stage,last_stage_change,owner", language="text")
    st.write("Dates must use YYYY-MM-DD. For example: `2026-11-10`. Each candidate ID must be unique.")
    st.download_button("Download sample CSV", SAMPLE.read_bytes(), file_name="sample_hiring_board.csv", mime="text/csv")

try:
    candidates, warnings = read_candidates(raw_data, analysis_date)
except ValueError as exc:
    st.error(f"The CSV couldn't be analyzed: {exc}")
    st.stop()

if warnings:
    st.warning(f"{len(warnings)} input row(s) needed attention and were skipped.")
    with st.expander("View input warnings"):
        for warning in warnings:
            st.write("- " + warning)
if not candidates:
    st.error("No valid candidate records were found. Check the CSV and analysis date.")
    st.stop()

alerts = assess_candidates(candidates, threshold, analysis_date)
counts = summarize(candidates)
urgent = sum(1 for a in alerts if a.priority == "Urgent")

st.subheader("2. Pipeline overview")
metric1, metric2, metric3, metric4 = st.columns(4)
metric1.metric("Valid candidates", counts["all"])
metric2.metric("Active candidates", counts["active"])
metric3.metric("Flagged to follow up", len(alerts))
metric4.metric("Urgent", urgent)

st.subheader("3. Follow-up queue")
if not alerts:
    st.success("No active candidate has reached the current stall threshold.")
    st.stop()

all_rows = [alert.for_export() for alert in alerts]
all_df = pd.DataFrame(all_rows)
priority_options = ["Urgent", "High", "Follow up"]
priority_filter = st.multiselect("Filter by priority", priority_options, default=priority_options)
search = st.text_input("Search candidate, role, owner or stage", placeholder="e.g., interview")
shown = all_df[all_df["Priority"].isin(priority_filter)].copy()
if search.strip():
    text = search.strip()
    relevant = shown[["Candidate", "Role", "Owner", "Stage"]]
    shown = shown[relevant.apply(lambda c: c.str.contains(text, case=False, regex=False)).any(axis=1)]

st.caption("Priority order is based on the explicit rules in the sidebar; the first row should be addressed first.")
show_table(shown)
st.caption("Spreadsheet safety: formula-like text in exported cells is neutralized for Excel-oriented viewing. Original values remain visible in the dashboard.")
st.download_button(
    "⬇ Download prioritized follow-up CSV",
    data=export_followups_csv(shown.to_dict(orient="records")),
    file_name=f"hiring_stall_followups_{analysis_date.isoformat()}.csv",
    mime="text/csv",
    disabled=shown.empty,
)

with st.expander("View counts by hiring stage"):
    stage_counts = all_df.groupby("Stage", sort=False).size().rename("Flagged candidates")
    st.bar_chart(stage_counts)

st.divider()
st.markdown("**Human review checkpoint:** Verify every recommendation before contacting candidates or changing pipeline records.")
st.caption("All analysis happens in this app; it does not send emails, modify hiring records, or call an external AI service.")