import argparse
import json
import os
import re
from ast import parse

import numpy as np
import pandas as pd
from wad_parsers import *
from wad_transform_maps import *

parser = argparse.ArgumentParser(description="Process Aselloidea occurrence data")
parser.add_argument("input_file", help="Input TSV file path")
parser.add_argument("output_file", help="Output JSON file path")

args = parser.parse_args()

colNames = {
    "rowID": "id",
    "LocID": "site_code",
    "VerbLoc": "site_verbatim",
    "Lat": "lat",
    "Long": "lon",
    "LatLongP": "precision",
    "ElevMin": "altitude",
    "LocRem": "site_comments",
    "EventDate": "event_date",
    "CollByPerson": "event_participants",
    "CollByGroup": "event_group",
    "Habita": "habitats",
    "Access": "access_points",
    "SamplEff": "sampling_effort",
    "SamplMet": "sampling_method",
    "Fixative": "fixative",
    "Program": "sampling_program",
    "Target": "sampling_target",
    "EventRem": "sampling_comments",
    "WaterTemp": "temperature",
    "WaterCond": "conductivity",
    "DateIden": "id_date",
    "IdenBy": "id_curator",
    "IdenAttri": "id_criterion",
    "IdenQualif": "id_qualifier",
    "identification_addendum": "id_addendum",
    "IdenVer": "id_verbatim",
    "TaxRank": "taxon_rank",
    "Genus": "genus",
    "Species": "species",
    "MOTU": "MOTU",
    "OccID": "occurrence_code",
    "BasRec": "occurrence_type",
    "RefBy": "reported_by",
    "OrgQuan": "organism_quantity",
    "OrgCount": "organism_count",
    "OccRem": "occurrence_comments",
    "AssRef": "references",
    "Gene": "gene",
    "AN": "accession_number",
    "Isolate": "specimen_voucher",
    "Origin_tax_name": "original_taxon_name",
    "Collection": "collection",
    "OriginalLink": "original_link",
    "DataSource": "data_source",
    "TypeStat": "type_status",
}


columns = list(colNames.values())
data = (
    pd.read_csv(
        args.input_file,
        # "data/Aselloidea/Aselloidea.tsv",
        sep="\t",
        decimal=",",
        na_values=["INCONNU"],
        index_col=False,
    )
    .rename(columns=colNames)[columns]
    .replace({np.nan: None})
)

data["event_date"] = data["event_date"].replace({None: "UNKNOWN"})
data["sampling_target"] = data["sampling_target"].replace({None: "UNKNOWN"})
data["species"] = data["species"].str.lower()

print(data)

taxa = [
    {
        "name": row.id_verbatim,
        "status": "Unclassified",
        "rank": row.taxon_rank,
        "parent": (
            row.genus if row.taxon_rank == "Species" else f"{row.genus} {row.species}"
        ),
    }
    for row in data[["id_verbatim", "genus", "species", "taxon_rank"]][
        data["id_verbatim"].str.contains(" aff.")
    ]
    .drop_duplicates()
    .itertuples()
]

taxa += [
    {
        "name": row.id_verbatim,
        "status": "Unclassified",
        "rank": row.taxon_rank,
        "parent": row.genus,
    }
    for row in data[["id_verbatim", "genus", "taxon_rank"]][
        data["id_verbatim"].str.contains(r" sp1?\. \(")
    ]
    .drop_duplicates()
    .itertuples()
]


def parse_biomat(code, df: pd.DataFrame):
    suffix = code.split("|")[-1]
    sequence = None
    if str(code).endswith(("NCBI", "PERSCOM")):
        db_reference = (
            {
                "db": "NCBI",
                "accession": df["accession_number"].iloc[0],
            }
            if suffix == "NCBI"
            else None
        )
        sequence = {
            "code": code,
            "gene": df["gene"].iloc[0],
            "referenced_in": [db_reference] if db_reference else None,
            "specimen_identifier": df["specimen_voucher"].iloc[0],
            "is_identifying": True,
        }
    bibref = parse_bib_ref(df)
    data_source = df["data_source"].iloc[0]
    if data_source:
        source_label = (
            data_sources.get(data_source.strip(), {}).get("label")
            or data_source.strip()
        )

    return {
        "code": code,
        "identification": parse_identification(df),
        "quantity": parse_specimen_quantity(
            df["organism_quantity"].iloc[0], df["organism_count"].iloc[0]
        ),
        "content_description": (
            df["occurrence_comments"].iloc[0]
            if df["occurrence_comments"].iloc[0]
            else None
        ),
        "verbatim_identification": df["original_taxon_name"].iloc[0]
        or df["id_verbatim"].iloc[0]
        or None,
        # "comments": df["occurrence_comments"].iloc[0],
        "collections": (
            [{"name": df["collection"].iloc[0]}] if df["collection"].iloc[0] else None
        ),
        "sources": ([source_label] if data_source else None),
        "published_in": bibref if bibref else None,
        "sequences": [sequence] if sequence else None,
        "type_status": (
            "Topotype"
            if df["type_status"].iloc[0] == "Specimens from type locality"
            else None
        ),
    }


invalid_sampling_targets = [
    "Stenasellus n sp rajasant",
    "Proasellus minoicus aff",
    "Proasellus lescherae cf",
    "Proasellus cantabricus aff",
    "Proasellus lagari aff",
    "Proasellus alavensis cf",
    "Proasellus escolai aff",
    "Macroinvertebrate",
    "Proasellus anophtalmus dalmatinus aff",
    "Proasellus n sp etcheberrigaray",
    "Proasellus pavani aff",
    "Proasellus n sp arpaon",
]


def parse_samplings(df: pd.DataFrame):
    samplings = []
    for (
        method,
        target,
        fixatives,
        habitats,
        access_point,
    ), s_group in df.groupby(
        [
            "sampling_method",
            "sampling_target",
            "fixative",
            "habitats",
            "access_points",
        ]
    ):
        access_point = access_points_map.get(access_point, None)

        biomaterials = []

        for code, group in s_group.groupby("occurrence_code"):
            if code not in drop_records:
                biomaterials.append(parse_biomat(code, group))

        sampling = {
            "methods": parse_methods(method),
            "target_taxa": [
                (
                    t
                    if t not in invalid_sampling_targets
                    else (
                        "Animalia"
                        if t and t.startswith("Macroinvertebrate")
                        else t.split(" ")[0]
                    )
                )
                for t in parse_sampling_target(target)
            ],
            "fixatives": parse_fixatives(fixatives),
            "access_points": [access_point],
            "habitats": list(
                set(habitats_map[habitats] or []).union(
                    access_points_habitats.get(access_point, []) or []
                    if access_point
                    else []
                )
            ),
            "duration": (
                int(s_group["sampling_effort"].iloc[0])
                if s_group["sampling_effort"].iloc[0] is not None
                else None
            ),
            "occurrences": biomaterials,
        }
        samplings.append(sampling)
    return samplings


result = []


for site_code, group in data.reset_index().groupby("site_code"):
    if len(set(group["lat"])) > 1:
        raise ValueError(f"Multiple latitudes for site {site_code}")
    if len(set(group["lon"])) > 1:
        raise ValueError(f"Multiple longitudes for site {site_code}")
    if len(set(group["precision"])) > 1:
        print(set(group["precision"]))
        raise ValueError(f"Multiple precisions for site {site_code}")
    coordinates = {
        "latitude": group["lat"].iloc[0],
        "longitude": group["lon"].iloc[0],
        "precision": parse_precision(group["precision"].iloc[0]),
    }

    samplings = []
    abiotics = []
    for date, ev_group in group.groupby("event_date"):
        if len(set(ev_group["sampling_program"])) > 1:
            print(set(ev_group["sampling_program"]))
            raise ValueError(
                f"Multiple sampling programs for site {site_code} at event {date}"
            )
        if len(set(ev_group["temperature"].dropna())) > 1:
            print(set(ev_group["temperature"].dropna()))
            raise ValueError(
                f"Multiple temperatures for site {site_code} at event {date}"
            )
        if len(set(ev_group["conductivity"].dropna())) > 1:
            print(set(ev_group["conductivity"].dropna()))
            raise ValueError(
                f"Multiple conductivities for site {site_code} at event {date}"
            )
        event = {
            "performed_on": parse_date(str(date)),
            "performed_by": (
                (
                    [
                        p.strip().title()
                        for p in ev_group["event_participants"].iloc[0].split("|")
                    ]
                    if ev_group["event_participants"].iloc[0]
                    else []
                )
                + (
                    [p.strip() for p in ev_group["event_group"].iloc[0].split("|")]
                    if ev_group["event_group"].iloc[0]
                    else []
                )
            )
            or None,
        }

        if ev_group["temperature"].iloc[0] is not None:
            abiotics.append(
                {
                    "param": "WATER-TEMP",
                    "value": float(ev_group["temperature"].iloc[0]),
                }
                | event
            )
        if ev_group["conductivity"].iloc[0] is not None:
            abiotics.append(
                {
                    "param": "CONDUCTIVITY",
                    "value": float(ev_group["conductivity"].iloc[0]),
                }
                | event
            )

        for sampling in parse_samplings(ev_group):
            samplings.append(sampling | event)

    result.append(
        {
            "code": site_code,
            "name": (
                group["site_verbatim"].iloc[0].title()
                if group["site_verbatim"].iloc[0]
                else None
            ),
            "coordinates": coordinates,
            "altitude": (
                int(group["altitude"].iloc[0])
                if group["altitude"].iloc[0] is not None
                else None
            ),
            "samplings": samplings,
            "abiotic_measurements": abiotics if abiotics else None,
        }
    )


taxa += [
    {
        "name": "Proasellus anophtalmus resavicae",
        "status": "Unreferenced",
        "rank": "Subspecies",
        "parent": "Proasellus anophtalmus",
    },
    {
        "name": "Proasellus anophtalmus rascicus",
        "status": "Unreferenced",
        "rank": "Subspecies",
        "parent": "Proasellus anophtalmus",
    },
    {
        "name": "Stenasellus virei rouchi",
        "status": "Unreferenced",
        "rank": "Subspecies",
        "parent": "Stenasellus virei",
    },
    {
        "name": "Stenasellus virei margalefi",
        "status": "Unreferenced",
        "rank": "Subspecies",
        "parent": "Stenasellus virei",
    },
]

dataset = {
    "label": "Aselloidea",
    "description": "Asellota is an order of isopod crustaceans. They are the largest order of isopods, with about 1,000 genera and over 3,000 species. They are found in marine environments worldwide, from the intertidal zone to the deep sea. They are typically small, with the largest species reaching 50 mm (2.0 in) in length. They are often found in sediments, where they burrow or live in tubes. They are scavengers, feeding on detritus and other organic material. They are an important part of the marine food chain, serving as prey for fish, birds, and other animals. They are also important in the decomposition of organic matter, helping to recycle nutrients in marine ecosystems.",
    "maintainers": ["fmalard"],
    "content": result,
    "bibliography": {
        verbatim: parse_article(verbatim)
        for verbatim in data["references"].dropna().unique().tolist()
    }
    | {
        saclier_article_verbatim: parse_article(saclier_article_verbatim),
        "Bou C. Personal Data (2002)": {
            "authors": ["Bou C."],
            "year": 2002,
            "title": "Personal communication",
            "verbatim": "Bou C. Personal Data (2002)",
        },
        "Magniez G. Personal Data (2002)": {
            "authors": ["Magniez G."],
            "year": 2002,
            "title": "Personal communication",
            "verbatim": "Magniez G. Personal Data (2002)",
        },
        "Sket B. Personal Data (2011)": {
            "authors": ["Sket B."],
            "year": 2011,
            "title": "Personal communication",
            "verbatim": "Sket B. Personal Data (2011)",
        },
        "Henry J.P. Personal Data (2001)": {
            "authors": ["Henry J.P."],
            "year": 2001,
            "title": "Personal communication",
            "verbatim": "Henry J.P. Personal Data (2001)",
        },
        "Ferreira D. Personal Data (2002)": {
            "authors": ["Ferreira D."],
            "year": 2002,
            "title": "Personal communication",
            "verbatim": "Ferreira D. Personal Data (2002)",
        },
        "Marmonier P. Personal Data (2002)": {
            "authors": ["Marmonier P."],
            "year": 2002,
            "title": "Personal communication",
            "verbatim": "Marmonier P. Personal Data (2002)",
        },
        "Dole Olivier M.J. Personal Data (2002)": {
            "authors": ["Dole Olivier M.J."],
            "year": 2002,
            "title": "Personal communication",
            "verbatim": "Dole Olivier M.J. Personal Data (2002)",
        },
        "Ginet R. Personal Data (2002)": {
            "authors": ["Ginet R."],
            "year": 2002,
            "title": "Personal communication",
            "verbatim": "Ginet R. Personal Data (2002)",
        },
        "Meyssonnier M. Personal Data (1996)": {
            "authors": ["Meyssonnier M."],
            "year": 1996,
            "title": "Personal communication",
            "verbatim": "Meyssonnier M. Personal Data (1996)",
        },
        "Malard F. Personal Data (2017)": {
            "authors": ["Malard F."],
            "year": 2017,
            "title": "Personal communication",
            "verbatim": "Malard F. Personal Data (2017)",
        },
        "Messana G. Personal Data (2012)": {
            "authors": ["Messana G."],
            "year": 2012,
            "title": "Personal communication",
            "verbatim": "Messana G. Personal Data (2012)",
        },
    },
    "taxa": taxa,
}


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
            if value is None:
                del d[key]
            else:
                del_none(value)
    return d


with open("res/Aselloidea_occurrences.json", "w+") as f:
    json.dump(del_none(dataset), f, indent=2)
