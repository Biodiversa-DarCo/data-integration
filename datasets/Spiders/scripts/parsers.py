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


def parse_date(date):
    """
    Parse a date string into a standard format (YYYY-MM-DD).
    """
    # Assuming the date is in the format YYYY-MM-DD
    if pd.isna(date) or pd.isnull(date) or not date or date == "UNKNOWN":
        return None
    date_str = str(date)
    d = date_str.split("-")
    if len(d) == 0:
        return None
    elif len(d) == 3:
        return {
            "date": {
                "year": int(d[0]),
                "month": int(d[1]),
                "day": int(d[2]),
            },
            "precision": "Day",
        }
    elif len(d) == 2:
        return {
            "date": {
                "day": 1,
                "year": int(d[0]),
                "month": int(d[1]),
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
    name = df["taxon_name"].iloc[0]
    if name == "Porrhomma myops":
        name = "Porrhomma myops Simon, 1884"
    return {
        "taxon": name if name else None,
        "confer": True if df["tax_id_confer"].iloc[0] else False,
        "performed_by": (
            df["identified_by"].iloc[0].split("; ")
            if not pd.isna(df["identified_by"].iloc[0])
            else None
        ),
    }


def parse_biomat(df: pd.DataFrame):
    refs = df["pub_verbatim"].dropna().unique()

    return {
        "identification": parse_identification(df),
        "specimen_quantity": (
            int(df["specimen_quantity"].sum())
            if not pd.isna(df["specimen_quantity"]).any()
            else None
        ),
        "collections": [
            {"name": collection} for collection in df["collection"].dropna().unique()
        ],
        "published_in": (
            [x for ref in refs.tolist() for x in ref.split("|")]
            if pd.isna(df["pub_DOI"].iloc[0])
            else []
        ),
        # split around "|" and flatten
        "dois": (
            [
                doi.strip()
                for doi in df["pub_DOI"].dropna().unique().tolist()[0].split("|")
                if not "NA" in doi
            ]
            if not pd.isna(df["pub_DOI"].iloc[0])
            else []
        ),
    }


def count_alphabetic(s: str) -> int:
    """
    Count the number of alphabetic characters in a string.
    """
    return len(re.findall(r"[A-Za-z]", s))
