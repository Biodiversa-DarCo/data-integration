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
        "identified_by": (
            [
                p.strip()
                for p in df["identifiedBy"].dropna().str.split("|").explode().unique()
            ]
            if df["identifiedBy"].iloc[0] is not None
            else None
        ),
        "confer": (
            df["id_confer"].iloc[0] if not pd.isna(df["id_confer"].iloc[0]) else None
        ),
        "addendum": (
            df["id_addendum"].iloc[0]
            if not pd.isna(df["id_addendum"].iloc[0])
            else None
        ),
        "taxon": df["taxon_name"].iloc[0] if df["taxon_name"].iloc[0] else None,
    }


def parse_biomat(df: pd.DataFrame):
    refs = df["references"].dropna().unique()
    data_sources = (
        df["datasetName"].dropna().unique().tolist()
        + df["data_repository"].dropna().unique().tolist()
    )

    return {
        "identification": parse_identification(df),
        "verbatim_identification": df["verbatim_identification"].iloc[0] or None,
        "sources": data_sources,
        "published_in": refs.tolist() if pd.isna(df["doi"].iloc[0]) else [],
        "doi": df["doi"].dropna().unique().tolist(),
    }


def count_alphabetic(s: str) -> int:
    """
    Count the number of alphabetic characters in a string.
    """
    return len(re.findall(r"[A-Za-z]", s))


def parse_article(verbatim: str):
    """
    Extracts author(s) and date from a verbatim string.
    """
    if verbatim is None:
        return None
    regex = re.compile(r"^([^\d]+)\s*\(?(\d{4})([\/\-]?\d{4})?\)?\.?")
    match = regex.match(verbatim)
    if match:
        authors = match.group(1).strip(" -_(")
        year = match.group(2).strip()
        mergedAuthorsList = []
        authorsList = re.split(r"(?:, ?| ?& ?| and |(?<=\.) (?=[A-Za-z]{2,}))", authors)
        for author in authorsList:
            author = author.strip().title()
            if re.search("[A-Za-z]{2}", author):
                mergedAuthorsList.append(author)
            elif len(mergedAuthorsList) > 0:
                mergedAuthorsList[-1] += ", " + author
            else:
                mergedAuthorsList.append(author)

        return {
            "authors": mergedAuthorsList,
            "year": int(year),
            "verbatim": verbatim,
        }
    else:
        return None
