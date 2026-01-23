import argparse
import json
from ast import parse

import numpy as np
import pandas as pd

from parsers import (
    count_alphabetic,
    parse_article,
    parse_biomat,
    parse_date,
    parse_precision,
)

parser = argparse.ArgumentParser(description="Process Aselloidea occurrence data")
parser.add_argument("input_file", help="Input TSV file path")
parser.add_argument("output_file", help="Output JSON file path")
parser.add_argument("--metadata", help="Metadata JSON file path")
parser.add_argument("--taxonomy", help="Taxonomy JSON file path")
parser.add_argument("--unreferenced_taxa", help="Unreferenced taxa JSON file path")

args = parser.parse_args(
    # ["datasets/Ostracoda/res/Ostracoda.tsv", "datasets/Ostracoda/res/Ostracoda.json"]
)
print(args)

data = pd.read_csv(args.input_file, sep="\t")
print(data)


results = []
site_id = 0
for [site_name, latitude, longitude], group in data.reset_index().groupby(
    ["site_name", "latitude", "longitude"]
):
    if len(set(group["latitude"])) > 1:
        raise ValueError(f"Multiple latitudes for site {site_name}")
    if len(set(group["longitude"])) > 1:
        raise ValueError(f"Multiple longitudes for site {site_name}")
    # if len(set(group["coord_precision"])) > 1:
    #     print(set(group["coord_precision"]))
    #     raise ValueError(f"Multiple precisions for site {site_name}")
    coordinates = {
        "latitude": group["latitude"].iloc[0],
        "longitude": group["longitude"].iloc[0],
        "precision": group["coord_precision"].iloc[0],
        # "precision": parse_precision(group["coord_precision"].iloc[0]),
    }

    samplings = []
    for date, ev_group in group.groupby("sampling_date"):
        occurrences = []
        for _, occ_row in ev_group.groupby("verbatim_identification"):
            occ = parse_biomat(occ_row)
            occurrences.append(occ)
        sampling = {
            "performed_on": parse_date(str(date)),
            "access_points": list(ev_group["access_points"].dropna().unique()),
            "habitats": list(
                ev_group["habitat"].dropna().str.split(", ").explode().unique()
            ),
            "occurrences": occurrences,
        }
        samplings.append(sampling)

    site_id += 1
    results.append(
        {
            "name": (
                site_name
                if count_alphabetic(site_name) > 1
                else f"Ostracoda_{site_name}"
            ),
            "code": f"Ostracoda_{site_id}",
            "coordinates": coordinates,
            "comments": (
                group["site_comments"].dropna().iloc[0]
                if not group["site_comments"].dropna().empty
                else None
            ),
            "altitude": (
                int(group["altitude"].iloc[0])
                if not pd.isna(group["altitude"].iloc[0])
                else None
            ),
            "samplings": samplings,
        }
    )


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


with open(args.taxonomy, "r") as f:
    taxonomy = json.load(f)

dataset = {
    "label": "Ostracoda",
    "description": "Ostracoda occurrence data from various sources.",
    "maintainers": ["pmarmonier", "nmori"],
    "content": del_none(results),
    "taxa": taxonomy,
    "bibliography": {
        verbatim: parse_article(verbatim)
        for verbatim in data["references"].dropna().unique().tolist()
    },
}

dataset["bibliography"][
    "Megyeri János: Ásott kutak hidrofaunisztikai vizsgálata. In: A Szegedi Tanárképző Főiskola tudományos közleményei 2. pp. 149-175. (1963)."
] = {
    "authors": ["Megyeri János"],
    "title": "Ásott kutak hidrofaunisztikai vizsgálata",
    "journal": "A Szegedi Tanárképző Főiskola tudományos közleményei",
    "year": 1963,
    "verbatim": "Megyeri János: Ásott kutak hidrofaunisztikai vizsgálata. In: A Szegedi Tanárképző Főiskola tudományos közleményei 2. pp. 149-175. (1963).",
}

with open(args.metadata, "r") as f:
    metadata = json.load(f)
    dataset.update(metadata)

with open(args.unreferenced_taxa, "r") as f:
    unreferenced_taxa = json.load(f)
    dataset["taxa"] += unreferenced_taxa

with open(args.output_file, "w") as f:
    json.dump(
        dataset,
        f,
        indent=2,
        ensure_ascii=False,
    )
