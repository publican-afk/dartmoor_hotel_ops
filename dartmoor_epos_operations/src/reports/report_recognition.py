import os
from typing import Tuple, List

from config import REPORT_KEYWORDS


def normalize_name(name: str) -> str:
    return name.lower().replace("_", " ").strip()


def recognize_report(filename: str) -> Tuple[str, List[str]]:
    name = normalize_name(os.path.splitext(filename)[0])
    recognized = []
    unknown = []

    for report_name, keywords in REPORT_KEYWORDS.items():
        if any(keyword in name for keyword in keywords):
            recognized.append(report_name)

    if not recognized:
        unknown.append(filename)

    return ", ".join(recognized), unknown
