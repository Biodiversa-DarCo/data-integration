# %%
import json
import pandas as pd
import numpy as np

from copepoda_parsers import parse_article

# import os
# print(os.getcwd())

# from copepoda_parsers import parse_article


colNames = {
    "ID": "id",
    "site_id": "site_code",
    "associatedReferences": "references",
}
columns = list(colNames.values()) + ["family"]

data = (
    pd.read_csv(
        "res/preprocessed.tsv",
        sep="\t",
        decimal=".",
        na_values=["NA", "NaN", ""],
    )
    .rename(columns=colNames)
    .replace({np.nan: None, pd.NA: None})
)
# Set access_point dtype to string to avoid issues with NaNs
data["access_point"] = data["access_point"].astype("string")
data["tax_id_qualifier"] = (
    data["tax_id_qualifier"].astype("string").replace({pd.NA: None})
)


# %%

results = []

for site_code, group in data.groupby("site_code"):
    if len(set(group["latitude"])) > 1:
        raise ValueError(f"Multiple latitudes for site {site_code}")
    if len(set(group["longitude"])) > 1:
        raise ValueError(f"Multiple longitudes for site {site_code}")
    if len(set(group["coord_precision"])) > 1:
        print(set(group["precision"]))
        raise ValueError(f"Multiple precisions for site {site_code}")
    coordinates = {
        "latitude": group["latitude"].iloc[0],
        "longitude": group["longitude"].iloc[0],
        "precision": group["coord_precision"].iloc[0],
    }

    country = group["country"].iloc[0]

    samplings = []

    for _, row in group.iterrows():

        biomat = {
            "identification": {
                "confer": "cf" in (row["tax_id_qualifier"] or ""),
                "taxon": row["scientificName"],
                "addendum": row["tax_id_addendum"],
            },
            "published_in": (
                [row["publication"]] if row["publication"] is not None else None
            ),
            "sources": [row["source"]] if row["source"] is not None else None,
        }

        samplings.append(
            {
                "access_points": (
                    row["access_point"].split(", ")
                    if not pd.isnull(row["access_point"])
                    else None
                ),
                "habitats": (
                    row["habitat"].split(", ")
                    if not pd.isnull(row["habitat"])
                    else None
                ),
                "target": {"kind": "Unknown"},
                "external_occurrences": [biomat],
                # "programs": parse_program(ev_group["sampling_program"].iloc[0]),
                # "comments": ev_group["sampling_comments"].iloc[0],
            }
        )

    results.append(
        {
            "code": site_code,
            "country": country,
            "coordinates": coordinates,
            "samplings": samplings,
        }
    )

# %%
with open("res/unclassified_taxa.json") as f:
    taxa = json.load(f)

dataset = {
    "label": "Copepoda",
    "description": "Copepods are a group of small crustaceans found in nearly every freshwater and saltwater habitat. Some species are planktonic (living in the water column), some are benthic (living on the sediments), several species have parasitic phases, and some continental species may live in limnoterrestrial habitats and other wet terrestrial places, such as swamps, under leaf fall in wet forests, bogs, springs, ephemeral ponds, puddles, damp moss, or water-filled recesses of plants (phytotelmata) such as bromeliads and pitcher plants. Many live underground in marine and freshwater caves, sinkholes, or stream beds. Copepods are sometimes used as biodiversity indicators. ",
    "maintainers": [],
    "occurrences": results,
    "import_clades": data["family"].unique().tolist(),
    "taxa": taxa,
    "data_sources": {
        "STOCH": {"label": "F. Stoch (2002) Collection (Rome)", "code": "STOCH"},
        "GALASSI": {"label": "D. Galassi Personal Collection", "code": "GALASSI"},
        "ATBI_MERCANTOUR": {
            "label": "ATBI Mercantour Database",
            "code": "ATBI_MERCANTOUR",
        },
    },
    "bibliography": {
        verbatim: parse_article(verbatim)
        for verbatim in data["publication"].dropna().unique().tolist()
    },
}


# %%
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


with open("res/Copepoda_occurrences.json", "w+") as f:
    json.dump(del_none(dataset), f, indent=2)
