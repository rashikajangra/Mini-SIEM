import streamlit as st
import pandas as pd
import datetime
from utils.log_detector import detect_log_type
from parser.ssh_parser import parse_ssh_log
from parser.apache_parser import parse_apache_log
from parser.windows_parser import parse_windows_log
from detector.rules import detect_brute_force, detect_apache_alerts, detect_windows_alerts
from utils.geoip import geolocate_alerts
from utils.emailer import alert_email
from utils.sample_logs import SSH_SAMPLE, APACHE_SAMPLE, WINDOWS_SAMPLE

#PAGE CONFIGURATION
st.set_page_config(page_title = "Mini SIEM Dashboard", layout = "wide")
st.title("Log Analyzer and Dashboard")
st.markdown("Upload a log file to begin analysis")

#SIDEBAR
st.sidebar.title("Settings")
st.sidebar.markdown("Configure your SIEM below")

#TRAINING MODE BUTTONS
st.sidebar.markdown("---")
st.sidebar.subheader("Training Mode")
st.sidebar.markdown("Load a sample log to learn:")

# session state keeps track of which sample is loaded
if "sample_content" not in st.session_state:
    st.session_state.sample_content = None
if "sample_type" not in st.session_state:
    st.session_state.sample_type = None

if st.sidebar.button("Load SSH Sample"):
    st.session_state.sample_content = SSH_SAMPLE
    st.session_state.sample_type = "ssh"

if st.sidebar.button("Load Apache Sample"):
    st.session_state.sample_content = APACHE_SAMPLE
    st.session_state.sample_type = "apache"

if st.sidebar.button("Load Windows Sample"):
    st.session_state.sample_content = WINDOWS_SAMPLE
    st.session_state.sample_type = "windows"

if st.sidebar.button("Clear Sample"):
    st.session_state.sample_content = None
    st.session_state.sample_type = None

st.sidebar.markdown("---")
st.sidebar.markdown("**Supported Log Types**")
st.sidebar.markdown("SSH Auth Logs")
st.sidebar.markdown("Apache Access Logs")
st.sidebar.markdown("Windows Event Logs")
st.sidebar.markdown("---")
st.sidebar.markdown("**Detection Rules**")
st.sidebar.markdown("- Brute Force (SSH/Windows)")
st.sidebar.markdown("- Suspicious Requests (Apache)")
st.sidebar.markdown("---")
st.sidebar.markdown("**Built With**")
st.sidebar.markdown("Python • Streamlit • Regex")

#FILE UPLOADER
uploaded_file = st.file_uploader("Upload Log File", type=["log", "txt"])

#sample or uploaded file
if st.session_state.sample_content:
    #use sample log
    file_content = st.session_state.sample_content
    log_type = st.session_state.sample_type
    st.info(f"Training Mode — Sample {log_type.upper()} log loaded")

elif uploaded_file is not None:
    #uploaded file
    st.success(f"File uploaded: {uploaded_file.name}")
    file_content = uploaded_file.read().decode("utf-8")
    log_type = detect_log_type(file_content).strip().lower()
    st.info(f"Detected log type: {log_type.upper()}")

else:
    # nothing loaded
    file_content = None
    log_type = None
    st.warning("No file uploaded. Upload a log file or load a sample from the sidebar.")

if file_content and log_type:

#PARSING
    if log_type == "ssh":
        parsed_logs = parse_ssh_log(file_content)
    elif log_type == "apache":
        parsed_logs = parse_apache_log(file_content)
    elif log_type == "windows":
        parsed_logs = parse_windows_log(file_content)
    else:
        st.error("Unknown log format. Supported: SSH, Apache, Windows.")
        parsed_logs = []

    if parsed_logs:

#DATAFRAME
        df = pd.DataFrame(parsed_logs)

#METRIC CARDS
        total = len(parsed_logs)
        col1, col2 = st.columns(2)
        col1.metric("Total Events", total)

        if log_type == "ssh":
            failed = len([x for x in parsed_logs if x["status"] == "Failed"])
            col2.metric("Failed Logins", failed)
            alerts = detect_brute_force(parsed_logs)

        elif log_type == "apache":
            errors = len([x for x in parsed_logs if x["status"] in ["404", "500"]])
            col2.metric("Error Responses", errors)
            alerts = detect_apache_alerts(parsed_logs)

        elif log_type == "windows":
            failed = len([x for x in parsed_logs if x["event_id"] == "4625"])
            col2.metric("Failed Logins", failed)
            alerts = detect_windows_alerts(parsed_logs)

        else:
            alerts = []

#LOG SUMMARY
        with st.expander("Log Summary"):
            st.markdown(f"**Total log entries:** {total}")
            if log_type == "ssh":
                most_attacked = df["username"].value_counts().idxmax()
                top_ip = df["ip"].value_counts().idxmax()
                st.markdown(f"**Most targeted username:** `{most_attacked}`")
                st.markdown(f"**Most active IP:** `{top_ip}`")
            elif log_type == "apache":
                top_ip = df["ip"].value_counts().idxmax()
                top_url = df["url"].value_counts().idxmax()
                st.markdown(f"**Most active IP:** `{top_ip}`")
                st.markdown(f"**Most requested URL:** `{top_url}`")
            elif log_type == "windows":
                top_ip = df["ip"].value_counts().idxmax()
                top_user = df["username"].value_counts().idxmax()
                st.markdown(f"**Most active IP:** `{top_ip}`")
                st.markdown(f"**Most targeted user:** `{top_user}`")

#ALERTS DASHBOARD
        st.subheader("ALERTS DASHBOARD")
        if alerts:
#add geolocation and timestamp to each alert
            alerts = geolocate_alerts(alerts)
            for alert in alerts:
                alert["detected_at"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            alert_df = pd.DataFrame(alerts)
            st.dataframe(alert_df)
            st.error(f"{len(alerts)} alert(s) detected!")

#CSV download button
            csv_data = alert_df.to_csv(index=False)
            st.download_button(
                label="Download Alerts as CSV",
                data=csv_data,
                file_name="siem_alerts.csv",
                mime="text/csv"
            )
        else:
            st.success("No alerts detected.")

#VISUAL ANALYSIS
        st.subheader("VISUAL ANALYSIS")
        chart_col1, chart_col2 = st.columns(2)

        with chart_col1:
            st.markdown("**Events by IP Address**")
            ip_counts = df["ip"].value_counts().reset_index()
            ip_counts.columns = ["IP Address", "Count"]
            st.bar_chart(ip_counts.set_index("IP Address"))

        with chart_col2:
            st.markdown("**Status Breakdown**")
            status_counts = df["status"].value_counts().reset_index()
            status_counts.columns = ["Status", "Count"]
            st.bar_chart(status_counts.set_index("Status"))

#EMAIL SIMULATION
        st.subheader("EMAIL ALERT SIMULATION")
        with st.expander("Simulate Alert Email"):
            receiver = st.text_input("Send alerts to (email)")
            if st.button("Simulate Email"):
                if alerts:
                    if receiver:
                        email_preview = alert_email(receiver, alerts)
                        st.success("Email simulation generated!")
                        st.code(email_preview)
                    else:
                        st.warning("Please enter a receiver email.")
                else:
                    st.info("No alerts to simulate right now.")

#SEARCH & FILTER
        st.subheader("SEARCH & FILTER LOGS")
        search_term = st.text_input("Search by keyword (IP, username, status...)")

        if log_type == "ssh":
            status_options = ["All", "Failed", "Accepted"]
        elif log_type == "apache":
            status_options = ["All", "200", "404", "500"]
        elif log_type == "windows":
            status_options = ["All", "Failure", "Success", "Logout"]
        else:
            status_options = ["All"]

        status_filter = st.selectbox("Filter by Status", status_options)

        filtered_df = df.copy()

        if search_term:
            mask = filtered_df.apply(
                lambda row: row.astype(str).str.contains(
                    search_term, case=False
                ).any(),
                axis=1
            )
            filtered_df = filtered_df[mask]

        if status_filter != "All":
            filtered_df = filtered_df[
                filtered_df["status"].astype(str) == status_filter
            ]

        st.markdown(f"**Showing {len(filtered_df)} of {len(df)} entries**")
        st.dataframe(filtered_df)

    else:
        st.warning("No log entries found. Please check your log file format.")

#FOOTER
st.markdown("---")
st.markdown(
    "<center>Mini SIEM Dashboard | Built with Python & Streamlit</center>",
    unsafe_allow_html=True
)