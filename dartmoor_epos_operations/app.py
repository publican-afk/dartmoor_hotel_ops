import os
from datetime import datetime

import pandas as pd
import plotly.express as px
import streamlit as st

from config import ALLOWED_EXTENSIONS, INCOMING_DIR, REPORT_KEYWORDS
from src.reports.report_recognition import recognize_report


def ensure_directories():
    os.makedirs(INCOMING_DIR, exist_ok=True)


def is_allowed_file(filename: str) -> bool:
    return filename.split(".")[-1].lower() in ALLOWED_EXTENSIONS


def load_file(file) -> pd.DataFrame:
    filename = file.name
    extension = filename.split(".")[-1].lower()
    try:
        if extension == "csv":
            return pd.read_csv(file)
        if extension in {"xls", "xlsx"}:
            return pd.read_excel(file)
    except Exception as exc:
        st.error(f"Unable to read file {filename}: {exc}")
        return pd.DataFrame()
    st.error(f"Unsupported file type: {filename}")
    return pd.DataFrame()


def save_uploaded_file(file):
    destination = os.path.join(INCOMING_DIR, file.name)
    with open(destination, "wb") as out_file:
        out_file.write(file.getbuffer())
    return destination


def dashboard_page(uploads):
    st.header("Dashboard")
    st.write("Welcome to Dartmoor EPOS Operations. Use the sidebar to upload reports and review them.")

    if uploads:
        counts = pd.DataFrame(uploads).value_counts().reset_index(name="count")
        fig = px.bar(counts, x=0, y="count", title="Recognised Report Types")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No recognised reports uploaded yet.")


def import_reports_page(uploads, unknowns):
    st.header("Import Reports")

    st.write("Upload CSV, XLS, or XLSX files and the app will save them and recognise report type from the filename.")

    uploaded_files = st.file_uploader(
        "Select report files to upload",
        type=["csv", "xls", "xlsx"],
        accept_multiple_files=True,
    )

    if uploaded_files:
        for file in uploaded_files:
            if not is_allowed_file(file.name):
                st.warning(f"Skipping unsupported file: {file.name}")
                continue

            saved_path = save_uploaded_file(file)
            df = load_file(file)
            report_name, unknown = recognize_report(file.name)

            if report_name:
                uploads.append(report_name)
                st.success(f"Uploaded and recognised report: {file.name} -> {report_name}")
            else:
                unknowns.extend(unknown)
                st.warning(f"Uploaded but not recognised: {file.name}")

            if not df.empty:
                st.write(f"Preview: {file.name}")
                st.dataframe(df.head(5))
            else:
                st.info("No preview available for this file.")

    if uploads:
        st.markdown("### Recognised Reports")
        for report in set(uploads):
            st.write(f"- {report}")

    if unknowns:
        st.markdown("### Unrecognised Reports")
        for report in set(unknowns):
            st.write(f"- {report}")


def reconciliation_page():
    st.header("Reconciliation")
    st.write("This section is reserved for future reconciliation workflows.")
    st.info("No live EPOS Now API connection is configured for Stage 1.")


def exceptions_page():
    st.header("Exceptions")
    st.write("Review exception records and invalid uploads here.")
    st.warning("Uploaded files that failed parsing are shown in the import page as invalid.")


def settings_page():
    st.header("Settings")
    st.write("Configure app behavior and data directories.")
    st.write(f"Incoming directory: `{INCOMING_DIR}`")
    st.write(f"Allowed file types: {', '.join(sorted(ALLOWED_EXTENSIONS))}")


def main():
    ensure_directories()

    st.set_page_config(page_title="Dartmoor EPOS Operations", layout="wide")
    st.title("Dartmoor EPOS Operations")

    pages = {
        "Dashboard": dashboard_page,
        "Import Reports": import_reports_page,
        "Reconciliation": reconciliation_page,
        "Exceptions": exceptions_page,
        "Settings": settings_page,
    }

    page = st.sidebar.selectbox("Select page", list(pages.keys()))
    st.sidebar.markdown("---")
    st.sidebar.write("Upload supported EPOS reports for recognition and review.")

    uploads = st.session_state.get("uploads", [])
    unknowns = st.session_state.get("unknowns", [])

    pages[page](uploads, unknowns) if page == "Import Reports" else pages[page]()

    st.session_state["uploads"] = uploads
    st.session_state["unknowns"] = unknowns


if __name__ == "__main__":
    main()
