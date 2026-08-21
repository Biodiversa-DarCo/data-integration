library(tidyverse)


dois <-
  read_lines("datasets/Asellidae/data/crossref.tsv") |>
  tibble(line = _) |>
  mutate(
    blank = str_trim(line) == "",
    block = cumsum(blank)
  ) |>
  filter(!blank) |>
  group_by(block) |>
  summarise(
    text = str_c(line, collapse = " "),
    .groups = "drop"
  ) |>
  mutate(
    doi = text |>
      str_extract(
        regex(
          "(?:https?://(?:dx\\.)?doi\\.org/|doi\\s*:?\\s*)?10\\.\\d{4,9}/\\S+",
          ignore_case = TRUE
        )
      ) |>
      str_remove(regex("^https?://(?:dx\\.)?doi\\.org/", ignore_case = TRUE)) |>
      str_remove(regex("^doi\\s*:?\\s*", ignore_case = TRUE)) |>
      str_remove("[[:punct:]]$") |>
      str_trim(),
    verbatim = text |>
      str_remove(
        regex(
          "(?:https?://(?:dx\\.)?doi\\.org/|doi\\s*:?\\s*)?10\\.\\d{4,9}/\\S+",
          ignore_case = TRUE
        )
      ) |>
      str_squish()
  ) |>
  filter(!is.na(doi)) |>
  select(verbatim, pub_doi = doi)

data <- read_tsv("datasets/Asellidae/data/Aselloidea.tsv", locale = locale(decimal_mark = ",")) |>
  mutate(
    sampling_participants = na_if(CollByPerson, "INCONNU") |>
      str_c(na_if(CollByGroup, "INCONNU"), sep = "|") |>
      na_if("|"),
    specimen_quantity = case_when(
      !is.na(OrgCount) ~ as.character(OrgCount),
      OrgQuan == "Plusierus dizaines d'individus (11-100)" ~ "11-100",
    ),
    occurrence_comments = if_else(str_starts(OccRem, "\\d"), NA_character_, OccRem),
    content_description = if_else(str_starts(OccRem, "\\d"), OccRem, NA_character_),
    coordinates_precision_m = LatLongP * 100000,
    sources = if_else(
      DataSource == "The World Asellidae Database",
      DataSource,
      str_c(DataSource, "The World Asellidae Database", sep = "|"),
    ),
    locality = str_to_title(str_c(Munici, Provin, ", ")),
    identified_by = str_to_title(na_if(IdenBy, "INCONNU")),
    sampling_targets = Target |>
      str_replace_all("_", " ") |>
      str_remove_all("INCONNU") |>
      str_remove_all("\\|$") |>
      str_replace("COMMUNITY", "Animalia") |>
      str_to_title() |>
      str_replace("Macroinvertebrate", "Arthropoda|Annelida|Mollusca|Platyhelminthes") |>
      str_remove_all("(?i)\\b(aff|cf|sp|n)\\b") |>
      str_squish() |>
      str_replace("Proasellus Arpaon", "Proasellus sp. (Arpaon)") |>
      str_replace("Proasellus Etcheberrigaray", "Proasellus sp. (Etcheberrigaray)") |>
      str_replace("Stenasellus Rajasant", "Stenasellus sp. (Rajasant)"),
    type_status = case_when(
      TypeStat == "Specimens from type locality" ~ "topotype",
      TRUE ~ TypeStat
    ),
  ) |>
  select(
    site_code = LocID,
    site_name = VerbLoc,
    locality,
    latitude = Lat,
    longitude = Long,
    coordinates_precision_m,
    altitude_m = ElevMin,
    event_date = EventDate,
    sampling_participants = sampling_participants, # rename to collectors ?
    access_points = Access,
    habitats = Habita,
    duration = SamplEff,
    sampling_methods = SamplMet,
    sampling_fixatives = Fixative,
    sampling_targets,
    sampling_comments = EventRem,
    occurrence_code = OccID,
    type_status,
    occurrence_comments,
    taxon_name = IdenVer,
    taxon_authorship = Authorship,
    taxon_rank = TaxRank,
    content_description,
    identification_date = DateIden,
    identification_verbatim = Origin_tax_name,
    identification_confer = IdenQualif,
    identification_addendum,
    identified_by,
    specimen_quantity = specimen_quantity,
    collections = Collection,
    sources = DataSource,
    water_temp = WaterTemp,
    water_conductivity = WaterCond,
    pub_verbatim = AssRef,
  ) |>
  mutate(
    identification_confer = (
      identification_confer == "cf."
    ),
    site_name = str_to_title(site_name) |> str_remove_all("[, \\.]+$"),
    sampling_methods = na_if(sampling_methods, "0 - INCONNU"),
    sampling_fixatives = na_if(sampling_fixatives, "0 - INCONNU"),
    access_points = str_to_title(access_points),
    habitats = str_to_title(habitats),
    pub_authors = str_extract(pub_verbatim, "^.*?(?=\\d{4})") |>
      str_remove_all("\\.$") |>
      str_squish(),
    pub_year = str_extract(pub_verbatim, "[0-9]{4}"),
    sampling_fixatives = na_if(sampling_fixatives, "0 - INCONNU"),
    sampling_methods = str_remove_all(sampling_methods, "0 - INCONNU\\|"),
    taxon_name = str_remove(taxon_name, " +sp\\. *$") |> str_remove("\\(Asellus\\) +") |> str_squish(),
    sampling_methods = str_replace(sampling_methods, "LAVAGE RACINE VEGETATION", "ROOTS WASHING") |>
      str_replace("SONDAGE BOU ROUCH", "BOU-ROUCH PUMP") |>
      str_replace("FILTRAGE DERIVE", "DRIFT FILTERING") |>
      str_replace("POMPAGE", "PUMPING") |>
      str_replace("FILTER PHREATOBIOLOGIQUE", "PHREATOBIOLOGICAL NET") |>
      str_replace("A VUE", "SIGHT") |>
      str_replace("CRYOCONSERVATION", "CRYO-CONSERVATION") |>
      str_replace("DRAGAGE", "DREDGING"),
    sampling_fixatives = str_replace(sampling_fixatives, "ALCOOL", "ALCOHOL") |>
      str_replace("SILICE", "SILICA") |>
      str_replace("AUTRE", "OTHER") |>
      str_replace("PAS DE MATERIAL FIXE", "NONE"),
    access_points = case_when(
      access_points == "Grotte" ~ "Cave",
      access_points == "0 - Inconnu" ~ NA_character_,
      access_points == "Puits" ~ "Well",
      access_points == "Source" ~ "Spring",
      access_points == "Zone Hyporheique" ~ "Hyporheic zone",
      access_points == "Riviere" ~ "River",
      access_points == "Fontaine" ~ "Fountain",
      access_points == "Captage Eau" ~ "Water catchment",
      access_points == "Canal" ~ "Channel",
      access_points == "Mine" ~ "Mine",
      access_points == "Autre" ~ NA_character_,
      access_points == "Aqueduc" ~ "Aqueduct",
      access_points == "Lac" ~ "Lake",
      access_points == "Ruisseau" ~ "Stream",
      access_points == "Lavoir" ~ "Washhouse",
      access_points == "Etang" ~ "Pond",
      access_points == "Marais Mare" ~ "Marsh",
      TRUE ~ access_points
    ),
  ) |>
  left_join(dois, by = c("pub_verbatim" = "verbatim"))
# mutate(
#   pub_title = if_else(is.na(pub_title),
#     str_extract(pub_verbatim, "(?<=\\d{4}\\.? ?).*") |>
#       str_split_i("\\.", 1) |>
#       str_squish(),
#     pub_title
#   ),
#   pub_journal = if_else(is.na(pub_journal),
#     str_extract(pub_verbatim, "(?<=\\d{4}\\.? ?).*") |>
#       str_split_i("\\.", 2) |>
#       str_squish(),
#     pub_journal
#   )
# )

data


data |> write_tsv("datasets/Asellidae/res/batch_wad.tsv", quote = "needed")


data |>
  select(pub_verbatim) |>
  distinct() |>
  arrange(pub_verbatim) |>
  write_tsv("datasets/Asellidae/res/pub_verbatim.tsv", quote = "needed")
