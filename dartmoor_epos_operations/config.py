import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INCOMING_DIR = os.path.join(BASE_DIR, "data", "incoming")
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")
ALLOWED_EXTENSIONS = {"csv", "xls", "xlsx"}

REPORT_KEYWORDS = {
    "End of Day": ["end of day", "eod", "day end", "dayend"],
    "Daily Sales": ["daily sales", "daily sales report", "daily_sales"],
    "Sales by Tender": ["sales by tender", "tender", "till sales"],
    "Refunds": ["refund", "refunds", "returned"],
    "Void Lines": ["void", "void lines", "voids"],
    "Petty Cash": ["petty cash", "pettycash"],
    "Turnover by Report Category": ["turnover by report category", "turnover", "report category"],
}
