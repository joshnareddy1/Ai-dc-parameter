import os
import streamlit as st
import pandas as pd

st.set_page_config(page_title="DC Parametric Optimization Dashboard", layout="wide")
st.title("⚡ DC Parametric Test Time Reduction Dashboard")

results_dir = "results"
data_dir = "data"

tabs = st.tabs(["📊 Scorecard & Metrics", "📈 Settling Sweep Analysis", "📝 Project Report"])

# Tab 1: Scorecards
with tabs[0]:
    st.subheader("Optimization Scorecard")
    scorecard_path = os.path.join(results_dir, "08_scorecard")
    found_scorecard = False
    if os.path.exists(scorecard_path):
        csv_files = [f for f in os.listdir(scorecard_path) if f.endswith(".csv")]
        if csv_files:
            selected_file = st.selectbox("Select Scorecard File", csv_files)
            df_score = pd.read_csv(os.path.join(scorecard_path, selected_file))
            st.dataframe(df_score, use_container_width=True)
            found_scorecard = True
    if not found_scorecard:
        st.info("No scorecard CSV files found in results/08_scorecard/.")

# Tab 2: Settling Sweep
with tabs[1]:
    st.subheader("Settling Sweep Curve")
    settling_csv = os.path.join(data_dir, "settling_sweep.csv")
    if os.path.exists(settling_csv):
        df_settling = pd.read_csv(settling_csv)
        st.write("Raw Settling Data Preview:")
        st.dataframe(df_settling.head(10), use_container_width=True)
        numeric_cols = df_settling.select_dtypes(include=["float64", "int64"]).columns.tolist()
        if len(numeric_cols) >= 2:
            col1, col2 = st.columns(2)
            with col1:
                x_axis = st.selectbox("X-Axis (Time/Sweep)", numeric_cols, index=0)
            with col2:
                y_axis = st.selectbox("Y-Axis (Settling Metric)", numeric_cols, index=1 if len(numeric_cols) > 1 else 0)
            st.line_chart(df_settling, x=x_axis, y=y_axis)
        else:
            st.line_chart(df_settling)
    else:
        st.warning(f"File {settling_csv} not found.")

# Tab 3: Report Preview
with tabs[2]:
    st.subheader("Project Report")
    report_file = os.path.join(results_dir, "PROJECT_REPORT.md")
    if os.path.exists(report_file):
        with open(report_file, "r") as f:
            st.markdown(f.read())
    else:
        st.info("No PROJECT_REPORT.md file found.")
