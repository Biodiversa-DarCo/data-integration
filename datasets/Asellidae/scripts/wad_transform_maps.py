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
    "Un seul individu": (1, 1),
    "Quelques individus (1-5)": (2, 5),
    "Une dizaine d'individus (6-10)": (6, 10),
    "Plusierus dizaines d'individus (11-100)": (11, 100),
    "Centaine d'individus (>100)": (101, 10000),
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
    "The Hypogean Crustacea Recording Scheme (UK)": {
        "label": "The Hypogean Crustacea Recording Scheme",
        "code": "HCRS",
        "url": "https://hcrs.brc.ac.uk/",
        "description": "The hypogean (subterranean) Crustacea recording scheme is a small scheme dealing with the subterranean macro-Crustacea (Malacostraca) found in the groundwater and aquatic cave habitats of the British Isles, including Ireland. ",
    },
}


drop_records = [
    "BRAGASELLUS_FRONTELLUM|ABOIM_201504_MOTU463",
    "BRAGASELLUS_FRONTELLUM|ABOIM_201504_MOTU466",
    "PROASELLUS_VALDENSIS|ARCINE_199104",
    "BRAGASELLUS_LAGARI|ARGONGE_201802",
    "PROASELLUS_SP|BREGAVE_200609",
    "Pslavus|BW31_201100_Bahrdt3_0|PERSCOM",
    "Pslavus|BW31_201100_Bahrdt4_0|PERSCOM",
    "Pslavus|BW7_201100_Bahrdt1_0|PERSCOM",
    "STENASELLUS_RACOVITZAI|CAVALLEG_000000",
    "PROASELLUS_SP1|CEZEBAGN_201605",
    "PROASELLUS_SYNASELLOIDES|CHATGAIL_201707_MOTU274",
    "BRAGASELLUS_COMASI|COBALLE2_200906_MOTU66",
    "PROASELLUS_ESCOLAI_AFF|COTILLAS_201010_MOTU181",
    "PROASELLUS_SP|DOVJEZ_200910",
    "PROASELLUS_SP1|DOVJEZ_200910",
    "PROASELLUS_SP2|DOVJEZ_200910",
    "PROASELLUS_SP|EMAMALET_2019005_MOTU274",
    "PROASELLUS_VALDENSIS|FARDELE_200602",
    "GALLASELLUS_HEILYI|FONTVEUV_200812_MOTU408",
    "GALLASELLUS_SP_A|FTAQUARI_201403_MOTU411",
    "Pcavaticus_GIRSTERK_201900_MN810701_ZFMKTIS21407|NCBI",
    "Pcavaticus_GIRSTERK_201900_MN810846_ZFMKTIS2510789|NCBI",
    "Pcavaticus_HAUSENWE_201404_MN810734_ZFMKTIS2501481|NCBI",
    "PROASELLUS_WALTERI|HMASCAIN_201605_MOTU320",
    "STENASELLUS_VIREI_VIREI|IZAIRE_198004",
    "Pslavus_KRITZENWE_202300_OQ538428_13|NCBI",
    "BRAGASELLUS_LAGARIOIDES|LAALFRAN_201300_MOTU74",
    "STENASELLUS_SP|LAALFRAN_201300",
    "PROASELLUS_SP|LAHAU_200703",
    "Pslavus_LOBAUWET_202300_OQ538426_No55|NCBI",
    "Akosswigi|MERAVIGL_000000_0_KT364293|NCBI",
    "Akosswigi|MERAVIGL_000000_0_KT364294|NCBI",
    "PROASELLUS_SYNASELLOIDES|MONTMAUR_201003_MOTU274",
    "Pcavaticus_MUHLBAGR_201406_MN810699_ZFMKTIS2501659|NCBI",
    "PROASELLUS_SP|MUNICHC_201503",
    "PROASELLUS_SP|NERETHY3_202206",
    "PROASELLUS_INTERMEDIUS|NIMIS_201608",
    "BRAGASELLUS_COMASI|PENDONES_200906_MOTU66",
    "GALLASELLUS_SP_A|PTSUREAU_201403_MOTU411",
    "PROASELLUS_SP|RIBNICE_200609_MOTU216",
    "PROASELLUS_WALTERI|ROSSFELD_201109",
    "PROASELLUS_CANTABRICUS|RUDRON_201010_MOTU124",
    "PROASELLUS_SP|SCENOIRE_201707",
    "PROASELLUS_N_SP2_SOSPEL|SOSPEL_201409",
    "PROASELLUS_N_SP_TORRACA1|TORRACA_201409",
    "PROASELLUS_N_SP_TORRACA2|TORRACA_201409",
    "PROASELLUS_SP|TRICHONI_200404",
    "PROASELLUS_AQUAECALIDAE_AFF|URROZWEL_198406",
    "PROASELLUS_N_SP_VINONVER|VINONVER_201509",
    "BRAGASELLUS_ESCOLAI|YUSOREIN_200906_MOTU79",
]
