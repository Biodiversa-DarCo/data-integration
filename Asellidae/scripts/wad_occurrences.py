import json
import os
import re
from ast import parse

import numpy as np
import pandas as pd
from wad_parsers import *
from wad_transform_maps import *
import argparse

parser = argparse.ArgumentParser(description="Process Aselloidea occurrence data")
parser.add_argument("input_file", help="Input TSV file path")
parser.add_argument("output_file", help="Output JSON file path")

args = parser.parse_args()

colNames = {
    "rowID": "id",
    "LocID": "site_code",
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
    "IdenVer": "id_verbatim",
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
}


columns = list(colNames.values())
data = (
    pd.read_csv(
        args.input_file,
        # "data/Aselloidea/Aselloidea.tsv",
        sep="\t",
        decimal=",",
        na_values=["INCONNU"],
    )
    .rename(columns=colNames)[columns]
    .replace({np.nan: None})
)

data["event_date"] = data["event_date"].replace({None: "UNKNOWN"})
data["sampling_target"] = data["sampling_target"].replace({None: "UNKNOWN"})

print(data)


def parse_biomat(code, df: pd.DataFrame):
    return {
        "code": code,
        "identification": parse_identification(df),
        "quantity": parse_specimen_quantity(
            df["organism_quantity"].iloc[0], df["organism_count"].iloc[0]
        ),
        "content_description": (
            f"{int(df['organism_count'].iloc[0])} specimens"
            if df["organism_count"].iloc[0]
            else None
        ),
        # "comments": df["occurrence_comments"].iloc[0],
        "in_collection": df["collection"].iloc[0],
        "original_source": (
            df["data_source"].iloc[0].strip() if df["data_source"].iloc[0] else None
        ),
        "published_in": parse_bib_ref(df),
    }


def parse_sequence(code, df: pd.DataFrame):
    suffix = code.split("|")[-1]
    origin = "DB" if suffix == "NCBI" else "PersCom"
    db_reference = (
        {
            "db": "NCBI",
            "accession": df["accession_number"].iloc[0],
            "is_origin": True,
        }
        if suffix == "NCBI"
        else None
    )
    return {
        "code": code,
        "gene": df["gene"].iloc[0],
        "origin": origin,
        "referenced_in": [db_reference] if db_reference else None,
        "published_in": parse_bib_ref(df),
        "specimen_identifier": df["specimen_voucher"].iloc[0],
        "original_taxon": df["original_taxon_name"].iloc[0],
        "identification": parse_identification(df),
    }


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
        sequences = []

        for code, group in s_group.groupby("occurrence_code"):
            if str(code).endswith(("NCBI", "PERSCOM")):
                sequences.append(parse_sequence(code, group))
            else:
                biomaterials.append(parse_biomat(code, group))

        sampling = {
            "methods": parse_methods(method),
            "target": parse_sampling_target(target),
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
            "external_biomats": biomaterials,
            "sequences": sequences,
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
                [p.strip() for p in ev_group["event_participants"].iloc[0].split("|")]
                if ev_group["event_participants"].iloc[0]
                else None
            ),
            "performed_by_groups": (
                [p.strip() for p in ev_group["event_group"].iloc[0].split("|")]
                if ev_group["event_group"].iloc[0]
                else None
            ),
        }

        abiotic = (
            {
                "temperature": ev_group["temperature"].iloc[0],
                "conductivity": ev_group["conductivity"].iloc[0],
            }
            if ev_group["temperature"].iloc[0] is not None
            or ev_group["conductivity"].iloc[0] is not None
            else None
        )
        if abiotic:
            abiotics.append(abiotic | event)

        samplings = parse_samplings(ev_group)
        for sampling in samplings:
            sampling |= event

    result.append(
        {
            "code": site_code,
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

organisations = {
    "NIB": {
        "name": "National Institute of Biology, Slovenia",
        "code": "NIB",
        "kind": "Lab",
    },
    "Uni-Lj": {
        "name": "University of Ljubljana, Slovenia",
        "code": "Uni-Lj",
        "kind": "Lab",
    },
    "INRAE": {
        "name": "Institut National de Recherche pour l'Agriculture, l'Alimentation et l'Environnement, France",
        "code": "INRAE",
        "kind": "Lab",
    },
    "SPELEO CLUB DIJON": {
        "name": "Spéléo Club de Dijon",
        "code": "SC Dijon",
        "kind": "Other",
    },
    "SPELEO GROUP JFB": {
        "name": "Spéléo Group JFB",
        "code": "Spéléo JFB",
        "kind": "Other",
    },
    "GROUPE SPELEOLOGIQUE LURON": {
        "name": "Groupe Spéléologique Luron",
        "code": "GSL",
        "kind": "Other",
    },
    "GBOL TEAM ZFMK": {
        "name": "German Barcode of Life (ZFMK team)",
        "code": "GBOL ZFMK",
        "kind": "Lab",
    },
    "BRITISH GEOLOGICAL SURVEY": {
        "name": "British Geological Survey",
        "code": "BGS",
        "kind": "Lab",
    },
    "UNION SPELEOL UNIV LONDRES": {
        "name": "London University Speleological Union",
        "code": "London IUS",
        "kind": "Other",
    },
    "DREAL LANGUEDOC ROUSSILLON": {
        "name": "Direction Régionale de l'Environnement, de l'Aménagement et du Logement Languedoc-Roussillon",
        "code": "DREAL LR",
        "kind": "Other",
    },
    "PARC NATIONAL DU MERCANTOUR": {
        "name": "Parc National du Mercantour",
        "code": "Parc Mercantour",
        "kind": "Other",
    },
    "AVEN GROUPE": {
        "name": "Aven Group",
        "code": "AVEN",
        "kind": "Other",
    },
    "GROUPE SPELEOLOGIQUE DU CCF": {
        "name": "Groupe Spéléologique du CCF",
        "code": "Spéléo CCF",
        "kind": "Other",
    },
}

taxa = [
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
    "occurrences": result,
    "organisations": organisations,
    "people": parse_person_columns(data),
    "bibliography": {
        verbatim: parse_article(verbatim)
        for verbatim in data["references"].dropna().unique().tolist()
    }
    | {saclier_article_verbatim: parse_article(saclier_article_verbatim)},
    "data_sources": data_sources,
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
