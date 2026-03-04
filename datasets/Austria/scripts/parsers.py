from numpy import isnan
import pandas as pd
import re


def parse_precision(precision: float) -> str:
    """
    Parse a precision string into a standard format.
    """
    if precision == 0.001:
        return "<100m"
    elif precision == 0.01:
        return "<1km"
    elif precision == 0.1:
        return "<10km"
    elif precision == 1:
        return "10-100km"
    else:
        return "Unknown"


def parse_date(date_str: str | None):
    """
    Parse a date string into a standard format (YYYY-MM-DD).
    """
    # Assuming the date is in the format YYYY-MM-DD
    if (
        pd.isna(date_str)
        or pd.isnull(date_str)
        or not date_str
        or date_str == "UNKNOWN"
    ):
        return None
    d = date_str.split("/")
    if len(d) == 0:
        return None
    elif len(d) == 3:
        return {
            "date": {
                "day": int(d[0]),
                "month": int(d[1]),
                "year": int(d[2]),
            },
            "precision": "Day",
        }
    elif len(d) == 2:
        return {
            "date": {
                "day": 1,
                "month": int(d[0]),
                "year": int(d[1]),
            },
            "precision": "Month",
        }
    else:
        return {
            "date": {
                "year": int(d[0]),
                "month": 1,
                "day": 1,
            },
            "precision": "Year",
        }


def parse_identification(df: pd.DataFrame):
    return {
        "taxon": df["taxon_name"].iloc[0] if df["taxon_name"].iloc[0] else None,
    }


def parse_biomat(df: pd.DataFrame):
    refs = df["pub_verbatim"].dropna().unique()

    return {
        "identification": parse_identification(df),
        "published_in": refs.tolist() if pd.isna(df["pub_DOI"].iloc[0]) else [],
        "dois": df["pub_DOI"].dropna().unique().tolist(),
    }


def count_alphabetic(s: str) -> int:
    """
    Count the number of alphabetic characters in a string.
    """
    return len(re.findall(r"[A-Za-z]", s))
