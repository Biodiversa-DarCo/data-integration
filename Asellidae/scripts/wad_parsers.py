import re
import pandas as pd
from wad_transform_maps import *

UNKNOWN_DATE = None


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
        return UNKNOWN_DATE
    d = date_str.split("-") if "-" in date_str else date_str.split("/")[::-1]
    if len(d) == 0:
        return UNKNOWN_DATE
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
                "year": int(d[0]),
                "month": int(d[1]),
                "day": 1,
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


def parse_sampling_target(target: str):
    """
    Parse a sampling target string into a standard format.
    """
    target = target.strip()
    if target == "COMMUNITY":
        return {"kind": "Community"}
    elif target in ("INCONNU", "UNKNOWN"):
        return {
            "kind": "Unknown",
        }
    else:
        return {
            "kind": "Taxa",
            "taxa": [
                re.sub(r" sp$", "", t.capitalize().replace("_", " "))
                for t in target.strip().split("|")
                if t != "INCONNU"
            ],
        }


def parse_person_list(persons: str | None) -> list[dict] | None:
    """
    Parse a list of person names into a list of dictionaries with first name, last name and organisation.
    """
    if persons is None:
        return None
    return [
        persons_map.get(p, parse_person(p))
        for p in persons.split("|")
        if p.strip() != "" and p.strip() != "INCONNU"
    ]


def parse_person(name: str) -> dict:
    """
    Parse a person name into a dictionary with first name, last name and organisation.
    """
    # Split the name into first and last name
    parts = name.title().split(" ")
    if len(parts) > 1:
        last_name = []
        first_name = []

        for i, part in enumerate(reversed(parts)):
            if len(part) == 1:
                first_name.append(part)
            else:
                first_name.reverse()
                last_name = parts[:(-i)]
                break
        last_name = " ".join(last_name)
        first_name = " ".join(first_name)
    else:
        last_name = parts[0]
        first_name = ""
    return {"first_name": first_name, "last_name": last_name, "organisation": None}


def parse_person_columns(df: pd.DataFrame) -> dict[str, dict]:
    persons = persons_map.copy()
    participants = df["event_participants"].dropna().unique()
    for p in participants:
        if p is None:
            continue
        parts = p.split("|")
        for person in parts:
            person = person.strip()
            if person not in persons:
                persons[person] = parse_person(person)
    id_curators = df["id_curator"].dropna().unique()
    for p in id_curators:
        if p is None:
            continue
        for person in p.split("|"):
            person = person.strip()
            if person not in persons:
                persons[person] = parse_person(person)
    return persons


def parse_methods(methods: str | None) -> list[str] | None:
    """
    Parse a string of methods into a list of methods.
    """
    if pd.isna(methods):
        return None
    return [
        smeth_map[m.strip()]
        for m in methods.split("|")
        if m.strip() != "" and m.strip() != "0 - INCONNU"
    ]


def parse_fixatives(fixatives: str) -> list[str]:
    return [
        fixatives_map[f]
        for f in fixatives.strip().split("|")
        if fixatives_map[f] is not None
    ]


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


def parse_program(program: str) -> list[str]:
    """
    Parse a program string into a list of programs.
    """
    if program == "Programme inconnu":
        return []
    else:
        return [program]


def parse_specimen_quantity(
    quantity_str: str, specimen_count: int | None
) -> str | None:
    """
    Parse a specimen quantity string into a standard format.
    """
    if specimen_count:
        if specimen_count == 1:
            return "One"
        elif specimen_count <= 5:
            return "Several"
        elif specimen_count <= 10:
            return "Ten"
        elif specimen_count <= 100:
            return "Tens"
        elif specimen_count > 100:
            return "Hundred"
    else:
        return quantity_map.get(quantity_str, None)


def parse_identification(df: pd.DataFrame):
    return {
        "identified_on": parse_date(df["id_date"].iloc[0]),
        "identified_by": (
            [p.strip() for p in df["id_curator"].iloc[0].split("|")][0]
            if df["id_curator"].iloc[0] is not None
            else None
        ),
        "confer": "cf" in (df["id_qualifier"].iloc[0] or ""),
        "taxon": re.sub(
            " sp.$",
            # r" sp\d*\.? ?(\([^\(\)]*\))?$",
            "",
            # re.sub(
            #     r"\([^\(\)]*\) | aff\.| form [A-Z]$",
            #     "",
            # re.sub(" (Asellus) ")
            df["id_verbatim"].str.replace(" (Asellus) ", " ").iloc[0],
            # df["id_verbatim"].iloc[0],
            # ),
        ).strip(),
    }


saclier_article_verbatim = "Saclier et al. 2023. The World Asellidae database and phylogeny: a collaborative backbone resource for comparative studies of subterranean life evolution. Molecular Ecology Resources, in press."


def parse_bib_ref(df: pd.DataFrame):
    refs = []
    if df["references"].iloc[0] is not None:
        refs.append(df["references"].iloc[0])
    if df["data_source"].iloc[0] == "The World Asellidae Database":
        refs.append(saclier_article_verbatim)
    return refs


def parse_article(verbatim: str):
    """
    Extracts author(s) and date from a verbatim string.
    """
    if verbatim is None:
        return None
    regex = re.compile(r"^([^\d]+)\s*\(?(\d{4})([\/\-]?\d{4})?\)?\.?")
    match = regex.match(verbatim)
    if match:
        authors = match.group(1).strip()
        year = match.group(2).strip()
        return {
            "authors": re.split(r"(?:, ?|(?<=\.) (?=[A-Za-z]{2,}))", authors),
            "year": int(year),
            "verbatim": verbatim,
        }
    else:
        return None
