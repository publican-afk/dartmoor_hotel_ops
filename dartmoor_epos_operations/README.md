# Dartmoor EPOS Operations

A Streamlit-based app for importing and recognising EPOS report files.

## Requirements

- Python 3.13
- Streamlit
- pandas
- openpyxl
- xlrd
- SQLAlchemy
- Plotly
- pytest

## Installation (Windows PowerShell)

1. Open PowerShell.
2. Navigate to the project folder:

```powershell
cd path\to\dartmoor_epos_operations
```

3. Create a virtual environment:

```powershell
python -m venv .venv
```

4. Activate the virtual environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

5. Install dependencies:

```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

## Running the app

In PowerShell with the virtual environment active:

```powershell
streamlit run app.py
```

## Running tests

```powershell
pytest
```

## Features

- Sidebar navigation with Dashboard, Import Reports, Reconciliation, Exceptions, and Settings.
- Upload CSV, XLS, XLSX files.
- Automatic report recognition using filename keywords.
- Saves uploaded files to `data/incoming`.
- Displays recognised and unrecognised reports.
- Handles invalid or unreadable files without crashing.
