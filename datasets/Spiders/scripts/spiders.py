import argparse
import json
import re
from ast import parse

import pandas as pd
from parsers import (
    count_alphabetic,
    parse_biomat,
    parse_date,
)

parser = argparse.ArgumentParser(description="Process Spiders occurrence data")
parser.add_argument("input_file", help="Input TSV file path")
parser.add_argument("output_file", help="Output JSON file path")
parser.add_argument("--unclassified", help="Unclassified taxa JSON file path")


args = parser.parse_args(
    # ["datasets/Spiders/data/dataset.tsv", "datasets/Spiders/res/Spiders.json"]
)
print(args)

data = pd.read_csv(args.input_file, sep="\t")
print(data)


def split_authors(author_string):
    """Split author string by separating author names.

    Handles formats like "Roewer, C. R., Jackson, W." correctly,
    splitting on "; ", ";", ",", ", ", or " " when followed by a new author (capital + lowercase).
    """
    if pd.isna(author_string):
        return []
    return [
        re.sub(r",\s*\.\s*$", "", author.strip())
        for author in re.split(r"[,;]?\s+(?=[A-Z][a-z])", author_string)
    ]


results = []
site_id = 0
row_ids = set()
for [site_name, latitude, longitude], group in data.reset_index().groupby(
    ["site_name", "latitude", "longitude"], dropna=False
):
    if len(group["latitude"].unique()) > 1:
        raise ValueError(f"Multiple latitudes for site {site_name}")
    if len(group["longitude"].unique()) > 1:
        raise ValueError(f"Multiple longitudes for site {site_name}")
    if len(group["coord_precision"].unique()) > 1:
        print(set(group["coord_precision"]))
        raise ValueError(f"Multiple precisions for site {site_name}")
    coordinates = {
        "latitude": group["latitude"].iloc[0],
        "longitude": group["longitude"].iloc[0],
        "precision": (
            group["coord_precision"].iloc[0]
            if not pd.isna(group["coord_precision"].iloc[0])
            else "Unknown"
        ),
        # "precision": parse_precision(group["coord_precision"].iloc[0]),
    }
    generated_site_name = (
        f"Spiders_{site_id}"
        if pd.isna(site_name)
        else (
            site_name
            if count_alphabetic(str(site_name)) > 1
            else f"Spiders_{site_name}"
        )
    )

    samplings = []
    for date, ev_group in group.groupby("sampling_date", dropna=False):
        if pd.isna(date):
            if len(ev_group) > 1:
                print(
                    f"Missing sampling date for site {generated_site_name}, treating {len(ev_group)} rows as separate sampling events"
                )
            for _, row in ev_group.iterrows():
                row_ids |= set([row["row_id"]])
                occ = parse_biomat(row.to_frame().T)
                sampling = {
                    "performed_on": None,
                    "access_points": (
                        [row["access_points"]]
                        if not pd.isna(row["access_points"])
                        else []
                    ),
                    "habitats": (
                        re.split(r", ?", row["habitat"])
                        if not pd.isna(row["habitat"])
                        else []
                    ),
                    "occurrences": [occ],
                }
                samplings.append(sampling)
            continue

        occurrences = []
        for _, occ_row in ev_group.groupby("taxon_name"):
            row_ids |= set(occ_row["row_id"].tolist())
            occ = parse_biomat(occ_row)
            occurrences.append(occ)
        sampling = {
            "performed_on": parse_date(date),
            "access_points": list(ev_group["access_points"].dropna().unique()),
            "habitats": list(
                ev_group["habitat"]
                .dropna()
                .str.split(", ?", regex=True)
                .explode()
                .unique()
            ),
            "occurrences": occurrences,
        }
        samplings.append(sampling)

    site_id += 1
    site = {
        "name": generated_site_name,
        "code": f"Spiders_{site_id}",
        "coordinates": coordinates,
        "locality": (
            group["locality"].dropna().iloc[0]
            if not group["locality"].dropna().empty
            else None
        ),
        "samplings": samplings,
    }
    results.append(site)


def del_none(d):
    """
    Delete keys with the value ``None`` in a dictionary, recursively.

    This alters the input so you may wish to ``copy`` the dict first.
    """
    if isinstance(d, list):
        d = [del_none(item) for item in d if item is not None]
        return d
    elif isinstance(d, dict):
        # Iterate through a copy of the dictionary’s items
        # so we can modify the original dictionary
        for key, value in list(d.items()):
            if value is None or (isinstance(value, list) and len(value) == 0):
                del d[key]
            else:
                del_none(value)
    return d


bibliography = {}
for pub_verbatim, group in data.groupby("pub_verbatim"):
    if pd.isna(pub_verbatim):
        continue
    # check that '|' is in the pub verbatim
    if "|" in str(pub_verbatim):
        print("found multipart pub verbatim")
        dois = (
            group["pub_DOI"].iloc[0].split("|")
            if not pd.isna(group["pub_DOI"].iloc[0])
            else []
        )
        for i, ref in enumerate(pub_verbatim.split("|")):
            if ref not in bibliography and (
                len(dois) < i + 1 or dois[i].strip() == "NA"
            ):
                bibliography[ref] = {
                    "authors": split_authors(
                        group["pub_authors"].iloc[0].split("|")[i]
                    ),
                    "year": (
                        int(group["pub_year"].iloc[0].split("|")[i])
                        if not pd.isna(group["pub_year"].iloc[0])
                        else None
                    ),
                    "title": (
                        group["pub_title"].iloc[0].split("|")[i]
                        if not pd.isna(group["pub_title"].iloc[0])
                        else None
                    ),
                    "journal": (
                        group["pub_journal"].iloc[0].split("|")[i]
                        if not pd.isna(group["pub_journal"].iloc[0])
                        else None
                    ),
                    "verbatim": ref,
                }
    else:
        bibliography[pub_verbatim] = {
            "authors": split_authors(group["pub_authors"].iloc[0]),
            "year": (
                int(group["pub_year"].iloc[0])
                if not pd.isna(group["pub_year"].iloc[0])
                else None
            ),
            "title": (
                group["pub_title"].iloc[0]
                if not pd.isna(group["pub_title"].iloc[0])
                else None
            ),
            "journal": (
                group["pub_journal"].iloc[0]
                if not pd.isna(group["pub_journal"].iloc[0])
                else None
            ),
            "verbatim": pub_verbatim,
        }


dataset = {
    "label": "Spiders",
    "description": "A dataset of subterranean spider occurrences in Europe.",
    "content": del_none(results),
    "bibliography": bibliography,
}

with open(args.unclassified, "r") as f:
    unclassified = json.load(f)
    dataset["taxa"] = unclassified + [
        {
            "name": "Typhlonesticus santinellii",
            "rank": "Species",
            "parent": "Typhlonesticus",
            "status": "Unreferenced",
            "authorship": "Isaia & Ribera, 2023",
        },
        {
            "name": "Troglohyphantes exspectatus",
            "rank": "Species",
            "parent": "Troglohyphantes",
            "status": "Unreferenced",
            "authorship": "Nadolny & Turbanov, 2025",
        },
        {
            "name": "Porrhomma ozrenense",
            "rank": "Species",
            "parent": "Porrhomma",
            "status": "Unreferenced",
            "authorship": "Komnenov, 2025",
        },
        {
            "name": "Leptoneta giputxi",
            "rank": "Species",
            "parent": "Leptoneta",
            "status": "Unreferenced",
            "authorship": "Prieto & Fernández-Pérez, 2023",
        },
        {
            "name": "Cybaeodes bernia",
            "rank": "Species",
            "parent": "Cybaeodes",
            "status": "Unreferenced",
            "authorship": "Ribera & Domènech, 2025",
        },
        {
            "name": "Cybaeodes gallinera",
            "rank": "Species",
            "parent": "Cybaeodes",
            "status": "Unreferenced",
            "authorship": "Ribera & Domènech, 2025",
        },
        {
            "name": "Poecilochroa exoculata",
            "rank": "Species",
            "parent": "Poecilochroa",
            "status": "Unreferenced",
            "authorship": "Lissner, 2024",
        },
        {
            "name": "Typhlonesticus angelicus",
            "rank": "Species",
            "parent": "Typhlonesticus",
            "status": "Unreferenced",
            "authorship": "Isaia & Ribera, 2023",
        },
        {
            "name": "Tenuiphantes sardous",
            "rank": "Species",
            "parent": "Tenuiphantes",
            "status": "Unreferenced",
            "authorship": "(Gozo, 1908)",
        },
        {
            "name": "Bisetifer tactus",
            "rank": "Species",
            "parent": "Bisetifer",
            "status": "Unreferenced",
            "authorship": "Nadolny & Turbanov, 2025",
        },
    ]

with open(args.output_file, "w") as f:
    json.dump(
        dataset,
        f,
        indent=2,
        ensure_ascii=False,
    )

print(f"[{len(row_ids)}]Missing rows : {set(data['row_id']) - row_ids}")
