import pytest

from src.reports.report_recognition import recognize_report


@pytest.mark.parametrize(
    "filename, expected",
    [
        ("end_of_day_summary.xlsx", "End of Day"),
        ("Daily Sales Report.csv", "Daily Sales"),
        ("sales_by_tender.xls", "Sales by Tender"),
        ("refunds_2025.xlsx", "Refunds"),
        ("VOID_LINES.xls", "Void Lines"),
        ("petty_cash_report.csv", "Petty Cash"),
        ("Turnover by report category.xlsx", "Turnover by Report Category"),
    ],
)
def test_recognize_report(filename, expected):
    report_name, unknown = recognize_report(filename)
    assert report_name == expected
    assert unknown == []


def test_unrecognized_report():
    report_name, unknown = recognize_report("unknown_report.csv")
    assert report_name == ""
    assert unknown == ["unknown_report.csv"]
