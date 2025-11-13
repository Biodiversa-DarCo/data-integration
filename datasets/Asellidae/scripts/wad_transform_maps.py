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

persons_map = {
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
    "EME D": {
        "first_name": "David",
        "last_name": "Eme",
        "organisation": "INRAE",
    },
    "NEGREA ST": {
        "first_name": "Ştefan",
        "last_name": "Negrea",
    },
    "PEARCE A E MCR": {
        "first_name": "A E",
        "last_name": "Pearce",
    },
    "MATSAKIS J TH": {
        "first_name": "J",
        "last_name": "Matsakis",
    },
    "ISSARTEL C": {
        "first_name": "Colin",
        "last_name": "Issartel",
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
    "Quelques individus (1-5)": "Several",
    "Une dizaine d'individus (6-10)": "Ten",
    "Plusierus dizaines d'individus (11-100)": "Tens",
    "Centaine d'individus (>100)": "Hundred",
}


data_sources = {
    "The World Asellidae Database": {
        "label": "The World Asellidae Database",
        "code": "WAD",
        "url": "https://gotit.univ-lyon1.fr/",
    },
    # "PASCALIS Database EC Project Contract Number EVK2-CT-2001-00121": {
    #     "label": "PASCALIS Database",
    #     "code": "PASCALIS",
    #     "description": "PASCALIS Database EC Project Contract Number EVK2-CT-2001-00121",
    # },
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
