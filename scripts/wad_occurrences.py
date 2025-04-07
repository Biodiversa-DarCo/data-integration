# %%
import re
from typing import TypedDict, Union
import numpy as np
import pandas as pd
import os
import re

from enum import Enum

colNames = {
    "rowID": "id",
    "LocID": "site_code",
    "Lat": "lat",
    "Long": "lon",
    "LatLongP": "precision",
    "ElevMin": "altitude",
    "LocRem": "site_comments",
    "EventDate": "event_date",
    "CollBy": "event_participants",
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

print(os.getcwd())

columns = list(colNames.values())
rawData = pd.read_csv(
    "data/Aselloidea/Aselloidea_All_Occurences_Europe_DarCo_For_Louis.tsv",
    sep="\t",
    decimal=",",
).rename(columns=colNames)[columns]

print(rawData)

# %%
habitats_map = {
    "0 - INCONNU": None,
    "AQUIFERE ALLUVIAL": ["Aquatic", "Subsurface", "Aquifer", "Alluvial"],
    "AQUIFERE FISSURE": ["Aquatic", "Subsurface", "Aquifer", "Fissured"],
    "AQUIFERE KARSTIQUE": ["Aquatic", "Subsurface", "Aquifer", "Karst"],
    "AQUIFERE POREUX": ["Aquatic", "Subsurface", "Aquifer", "Porous"],
    "EAU DOUCE DE SURFACE": ["Surface", "Aquatic", "Freshwater"],
    "EAU DOUCE SOUTERRAINE": ["Subsurface", "Aquatic", "Freshwater"],
    "EAU SALEE SOUTERRAINE": ["Subsurface", "Aquatic", "Saltwater"],
    "SYSTEME LENTIQUE": ["Aquatic", "Lentic"],
    "SYSTEME LOTIQUE": ["Aquatic", "Lotic"],
    "ZONE HYPORHEIQUE": ["Aquatic", "Subsurface", "Aquifer", "Hyporheic zone"],
    "ZONE NON SATUREE KARSTIQUE": [
        "Aquatic",
        "Subsurface",
        "Aquifer",
        "Karst",
        "Unsaturated",
    ],
    "ZONE SATUREE KARSTIQUE": [
        "Aquatic",
        "Subsurface",
        "Aquifer",
        "Karst",
        "Saturated",
    ],
}

access_points_map = {
    "0 - INCONNU": None,
    "AUTRE": None,
    "ZONE HYPORHEIQUE": "Hyporheic zone",
    "AQUEDUC": "Aqueduct",
    "CANAL": "Canal",
    "CAPTAGE EAU": "Water catchment",
    "ETANG": "Pond",
    "FONTAINE": "Fountain",
    "GROTTE": "Cave",
    "LAC": "Lake",
    "LAVOIR": "Wash house",
    "MARAIS MARE": "Marsh",
    "MINE": "Mine",
    "PUITS": "Well",
    "RIVIERE": "River",
    "RUISSEAU": "Stream",
    "SOURCE": "Spring",
    "TUNNEL": "Tunnel",
}

persons = {
    "ZAGMAJSTER M": {
        "first_name": "Maja",
        "last_name": "Zagmajster",
        "organisation": "Uni-Lj",
    },
    "MALARD F": {
        "first_name": "Florian",
        "last_name": "Malard",
        "organisation": "LEHNA",
    },
    "MORI N": {"first_name": "Nataša", "last_name": "Mori", "organisation": "NIB"},
    "LEFEBURE T": {
        "first_name": "Tristan",
        "last_name": "Lefebure",
        "organisation": "LEHNA",
    },
    "DELIC T": {"first_name": "Teo", "last_name": "Delić", "organisation": "Uni-Lj"},
    "DOUADY C": {
        "first_name": "Christophe",
        "last_name": "Douady",
        "organisation": "LEHNA",
    },
    "SACLIER N": {
        "first_name": "Natanaëlle",
        "last_name": "Saclier",
        "organisation": "LEHNA",
    },
    "CREUZE DES CHATELLIERS M": {
        "first_name": "Michel",
        "last_name": "Creuzé des Châtelliers",
        "organisation": "LEHNA",
    },
    "MERMILLOD BLONDIN F": {
        "first_name": "Florian",
        "last_name": "Mermillod-Blondin",
        "organisation": "LEHNA",
    },
    "FRANCOIS C": {
        "first_name": "Clémentine",
        "last_name": "François",
        "organisation": "LEHNA",
    },
}

smeth_map = {
    "0 - INCONNU": None,
    "A VUE": "Sight",
    "SURBER": "Surber net",
    "FILTRAGE DERIVE": "Drift filtering",
    "LAVAGE RACINE VEGETATION": "Root washing",
    "FILET PHREATOBIOLOGIQUE": "Phreatobiological net",
    "DRAGAGE": "Dredging",
    "POMPAGE": "Pumping",
    "SONDAGE BOU ROUCH": "Bou-Rouch pump",
    "SONDAGE KARAMAN CHAPPUIS": "Karaman-Chappuis",
}

# %%


def parse_person(name: str) -> dict:
    """
    Parse a person name into a dictionary with first name, last name and organisation.
    """
    # Split the name into first and last name
    parts = name.title().split(" ")
    if len(parts) > 1:
        last_name = " ".join(parts[:-1])
        first_name = parts[-1]
    else:
        last_name = parts[0]
        first_name = ""
    return {"first_name": first_name, "last_name": last_name, "organisation": None}


DatePrecision = Enum("DatePrecision", ["Day", "Month", "Year", "Unknown"])
CompositeDate = TypedDict("CompositeDate", {"year": int, "month": int, "day": int})
DateWithPrecision = TypedDict(
    "DateWithPrecision",
    {
        "date": CompositeDate,
        "precision": DatePrecision,
    },
)

UNKNOWN_DATE: DateWithPrecision = {
    "date": {
        "year": 1,
        "month": 1,
        "day": 2000,
    },
    "precision": DatePrecision.Unknown,
}


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


def parse_date(date_str: str | None) -> DateWithPrecision:
    """
    Parse a date string into a standard format (YYYY-MM-DD).
    """
    # Assuming the date is in the format YYYY-MM-DD
    if pd.isna(date_str) or pd.isnull(date_str) or not date_str:
        return UNKNOWN_DATE
    d = date_str.split("-") if "-" in date_str else date_str.split("/")[::-1]
    print(d)
    if len(d) == 0:
        return UNKNOWN_DATE
    elif len(d) == 3:
        return {
            "date": {
                "year": int(d[0]),
                "month": int(d[1]),
                "day": int(d[2]),
            },
            "precision": DatePrecision.Day,
        }
    elif len(d) == 2:
        return {
            "date": {
                "year": int(d[0]),
                "month": int(d[1]),
                "day": 1,
            },
            "precision": DatePrecision.Month,
        }
    else:
        return {
            "date": {
                "year": int(d[0]),
                "month": 1,
                "day": 1,
            },
            "precision": DatePrecision.Year,
        }


def parse_sampling_target(target: str):
    """
    Parse a sampling target string into a standard format.
    """
    target = target.strip()
    if target == "COMMUNITY":
        return {"kind": "Community"}
    elif target == "INCONNU":
        return {
            "kind": "Unknown",
        }
    else:
        return {
            "kind": "Taxa",
            "taxa": [
                t.capitalize().replace("_", " ")
                for t in target.strip().split("|")
                if t != "INCONNU"
            ],
        }


fixatives_map = {
    "0 - INCONNU": None,
    "AUTRE": None,
    "PAS DE MATERIEL FIXE": None,
    "ALCOOL": "Ethanol",
    "FORMOL": "Formaldehyde",
    "CRYOCONSERVATION": "Cryo-conservation",
    "SILICE": "Silica",
    "RNA LATER": "RNA later",
}

access_points_habitats = {
    "Well": ["Aquatic", "Subsurface", "Freshwater"],
    "Wash house": ["Aquatic", "Freshwater"],
    "Fountain": ["Aquatic", "Freshwater"],
    "Lake": ["Aquatic", "Surface", "Lentic"],
    "Marsh": ["Aquatic", "Surface", "Lentic"],
    "Pond": ["Aquatic", "Surface", "Lentic"],
    "River": ["Aquatic", "Surface", "Freshwater", "Lotic"],
    "Stream": ["Aquatic", "Freshwater", "Lotic"],
    "Spring": ["Aquatic", "Freshwater", "Lotic"],
    "Canal": ["Aquatic", "Freshwater"],
    "Aqueduct": ["Aquatic", "Freshwater"],
    "Cave": ["Subsurface"],
    "Tunnel": ["Subsurface"],
    "Mine": ["Subsurface"],
    "Water catchment": ["Aquatic", "Freshwater"],
    "Hyporheic zone": ["Aquatic", "Hyporheic zone", "Aquifer", "Subsurface"],
}

quantity_map = {
    "Un seul individu": "One",
    "Quelques individus (1-5)": "Few",
    "Une dizaine d'individus": "Ten",
    "Plusierus dizaines d'individus (11-100)": "Tens",
    "Centaine d'individus (>100)": "Hundred",
}


def parse_fixatives(fixatives: str) -> list[str]:
    return [
        fixatives_map[f]
        for f in fixatives.strip().split("|")
        if fixatives_map[f] is not None
    ]


data_sources = {
    "The World Asellidae Database": {
        "label": "The World Asellidae Database",
        "code": "WAD",
        "url": "https://gotit.univ-lyon1.fr/",
    },
    "PASCALIS Database EC Project Contract Number EVK2-CT-2001-00121": {
        "label": "PASCALIS Database",
        "code": "PASCALIS",
        "description": "PASCALIS Database EC Project Contract Number EVK2-CT-2001-00121",
    },
    "CKmap Distribuzione della Fauna Italiana Checklist and distribution of 10000 species of the Italian fauna": {
        "label": "CKmap database",
        "code": "CKMAP",
        "description": "CKmap Distribuzione della Fauna Italiana Checklist and distribution of 10000 species of the Italian fauna",
    },
    "Bou C. Personal Data (2002)": {
        "label": "Bou C. Personal Data (2002)",
        "code": "BOU_2002",
    },
    "Magniez G. Personal Data (2002)": {
        "label": "Magniez G. Personal Data (2002)",
        "code": "MAGNIEZ_2002",
    },
    "Sket B. Personal Data (2011)": {
        "label": "Sket B. Personal Data (2011)",
        "code": "SKET_2001",
    },
    "Henry J.P. Personal Data (2001)": {
        "label": "Henry J.P. Personal Data (2001)",
        "code": "HENRY_2001",
    },
    "Ferreira D. Personal Data (2002)": {
        "label": "Ferreira D. Personal Data (2002)",
        "code": "FERREIRA_2002",
    },
    "Marmonier P. Personal Data (2002)": {
        "label": "Marmonier P. Personal Data (2002)",
        "code": "MARMONIER_2002",
    },
    "Dole Olivier M.J. Personal Data (2002)": {
        "label": "Dole Olivier M.J. Personal Data (2002)",
        "code": "DOLE_OLIVIER_2002",
    },
    "Ginet R. Personal Data (2002)": {
        "label": "Ginet R. Personal Data (2002)",
        "code": "GINET_2002",
    },
    "Meyssonnier M. Personal Data (1996)": {
        "label": "Meyssonnier M. Personal Data (1996)",
        "code": "MEYSSONNIER_1996",
    },
    "Malard F. Personal Data (2017)": {
        "label": "Malard F. Personal Data (2017)",
        "code": "MALARD_2017",
    },
    "Messana G. Personal Data (2012)": {
        "label": "Messana G. Personal Data (2012)",
        "code": "MESSANA_2012",
    },
    "The Hypogean Crustacea Recording Scheme (UK)": {
        "label": "The Hypogean Crustacea Recording Scheme",
        "code": "HCRS",
        "url": "https://hcrs.brc.ac.uk/",
        "description": "The hypogean (subterranean) Crustacea recording scheme is a small scheme dealing with the subterranean macro-Crustacea (Malacostraca) found in the groundwater and aquatic cave habitats of the British Isles, including Ireland. ",
    },
}


data = rawData.assign(
    # habitats=lambda v: v["habitats"].apply(lambda x: habitats_map.get(x, None)),
    # access_points=lambda v: v["access_points"].apply(
    #     lambda x: access_points_map.get(x, None)
    # ),
    # event_participants=lambda v: v["event_participants"].apply(
    #     lambda x: [
    #         persons.get(p.strip(), parse_person(p))
    #         for p in x.split("|")
    #         if p.strip() != ""
    #     ]
    # ),
    precision=lambda v: v["precision"].apply(lambda x: "Unknown" if np.isnan(x) else x),
    # event_date_parsed=lambda v: v["event_date"]
    # .convert_dtypes(convert_string=True)
    # .apply(parse_date),
).sort_index()


data.index

dups = data.iloc[data.index.duplicated()]


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
        "precision": group["precision"].iloc[0],
    }

    events = []
    for date, ev_group in group.groupby("event_date"):
        if date == "01/06/2013":
            continue
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
        abiotic = (
            {
                "temperature": ev_group["temperature"].iloc[0],
                "conductivity": ev_group["conductivity"].iloc[0],
            }
            if not np.isnan(ev_group["temperature"].iloc[0])
            and not np.isnan(ev_group["conductivity"].iloc[0])
            else None
        )

        samplings = []

        for (
            method,
            target,
            fixatives,
            habitats,
            access_point,
        ), s_group in ev_group.groupby(
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
            for biomat, bm_group in s_group.groupby("occurrence_code"):

                identification = {
                    "identified_on": parse_date(bm_group["id_date"].iloc[0]),
                    "identified_by": [
                        parse_person(person)
                        for person in bm_group["id_curator"].iloc[0].split("|")
                    ],
                    "taxon": re.sub(r"\(\w+\) ", "", bm_group["id_verbatim"].iloc[0]),
                }

                biomat = {
                    "code": biomat,
                    "identification": identification,
                    "quantity": quantity_map.get(
                        bm_group["organism_quantity"].iloc[0], None
                    ),
                    "comments": bm_group["occurrence_comments"].iloc[0],
                    "in_collection": bm_group["collection"],
                    "original_source": data_sources.get(bm_group["data_source"], None),
                    "published_in": [bm_group["references"]],
                }
                biomaterials.append(biomat)

            sampling = {
                "methods": parse_methods(method),
                "target": parse_sampling_target(target),
                "fixatives": parse_fixatives(fixatives),
                "access_points": access_point,
                "habitats": set(habitats_map[habitats] or []).union(
                    access_points_habitats.get(access_point, []) or []
                    if access_point
                    else []
                ),
                "sampling_effort": s_group["sampling_effort"].iloc[0],
                "biomaterials": biomaterials,
            }
            samplings.append(sampling)

        events.append(
            {
                "performed_on": parse_date(str(date)),
                "participants": ev_group["event_participants"].iloc[0],
                "programs": ev_group["sampling_program"].iloc[0],
                "abiotic_sampling": abiotic,
                "samplings": samplings,
                "comments": ev_group["sampling_comments"].iloc[0],
            }
        )

    result.append(
        {
            "site_code": site_code,
            "coordinates": coordinates,
            "altitude": group["altitude"].iloc[0],
            "events": events,
        }
    )

result


# .assign(
#     coordinates=lambda v: v.apply(
#         lambda x: {
#             "latitude": x["lat"],
#             "longitude": x["lon"],
#             "precision": x["precision"],
#         },
#         axis=1,
#     ),
# ).drop(
#     columns=["lat", "lon", "precision"]
# )
# .apply(lambda x: {
#     'lat': x['lat'],
#     'lon': x['lon'],
#     'precision': x['precision'],
# })
# .to_frame()

# data
# data

# %%
