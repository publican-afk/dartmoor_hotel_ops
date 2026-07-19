import os
import re
from typing import List, Tuple


REPORT_PREFIXES = {
    "End of Day": ("endofday", "eod", "dayend"),
    "Daily Sales": ("dailysales", "dailysalesreport"),
    "Sales by Tender": ("salesbytender", "tendersales", "tillsales"),
    "Refunds": ("refunds", "refund", "returned"),
    "Void Lines": ("voidlines", "voids", "void"),
    "Petty Cash": ("pettycashreport", "pettycash"),
    "Turnover by Report Category": (
        "turnoverbyreportcategory",
        "reportcategoryturnover",
    ),
}


def normalize_name(name: str) -> str:
    """Return a filename-safe comparison value with punctuation removed."""
    stem = os.path.splitext(os.path.basename(name))[0]
    return re.sub(r"[^a-z0-9]+", "", stem.lower())


def recognize_report(filename: str) -> Tuple[str, List[str]]:
    """Recognise an EPOS Now report from the beginning of its filename."""
    normalized_name = normalize_name(filename)

    for report_name, prefixes in REPORT_PREFIXES.items():
        if any(normalized_name.startswith(prefix) for prefix in prefixes):
            return report_name, []

    return "", [filename]
