library(tidyverse)

args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 2) {
  stop("Usage: copepoda.R <input_file.tsv> <locality_fix.tsv> <reference_fix.tsv> <output_file.tsv>")
}
input_file <- args[1]
locality_fix_file <- args[2]
reference_fix_file <- args[3]
output_file <- args[4]

locality_fix <- read_tsv(locality_fix_file)
reference_fix <- read_tsv(reference_fix_file)

data <- read_tsv(input_file, na = c("NULL", "Unclear", "unclear", "??", "?", "Unknown")) |>
  left_join(locality_fix, by = "Locality") |>
  mutate(
    Locality = ifelse(!is.na(Locality_fixed), Locality_fixed, Locality) |> str_replace("�kocjanske", "Škocjanske")
  ) |>
  mutate(
    Locality = case_when(
      Locality == "Keprnický brook - ?eská Vyso?ina" ~ "Keprnický brook - Česká Vysočina",
      str_squish(Locality) == str_squish("Lede? nad Sázavou town, Šeptouchovská village, Vyso?ina Region,  cave in Septouchovska") ~ "Ledeč nad Sázavou town, Šeptouchovská village, Vysočina Region, cave in Septouchovska",
      str_starts(Locality, "Orcia river, three different sites across the river") ~ "Orcia river, three different sites across the river",
      TRUE ~ Locality
    )
  ) |>
  left_join(reference_fix, by = "associatedReferences") |>
  mutate(
    associatedReferences = ifelse(!is.na(associatedReferences_fixed), associatedReferences_fixed, associatedReferences) |>
      str_remove(", \\?\\??$")
  ) |>
  select(-Locality_fixed, -associatedReferences_fixed) |>
  mutate(
    Modif_taxonomy_FM = ifelse(Modif_taxonomy_FM == "yes", T, F),
    taxon_rank = case_when(
      !is.na(infraspecificEpithet) ~ "Subspecies",
      !is.na(specificEpithet) & specificEpithet != "sp." ~ "Species",
      !is.na(subgenus) ~ "Subgenus",
      TRUE ~ "Genus"
    ),
  ) |>
  select(-habitat, -locationRemarks, -geodeticDatum, -Easting_EPSG3035, -Northing_EPSG3035, -Coord.Validator) |>
  rename(
    habitat = Habitat_Florian,
    access_point = Access_Florian,
    longitude = decimalLongitude,
    latitude = decimalLatitude,
    coord_precision = Coord.Uncertainty,
    tax_id_qualifier = FM_dwc_identificationQualifier,
    tax_id_addendum = FM_identification_addendum
  ) |>
  mutate(
    coord_precision = case_when(
      coord_precision == "0.5 km" ~ 500,
      coord_precision == "1 km" ~ 1000,
      coord_precision == "2 km" ~ 2000,
      coord_precision == "3 km" ~ 3000,
      coord_precision == "5 km" ~ 5000,
      coord_precision == "0.1 km" ~ 100,
      coord_precision == "Catchment" ~ 1000,
      coord_precision == "20 km" ~ 20000,
      coord_precision == "Comm.Centr" ~ 10000,
      coord_precision == "0.2 km" ~ 200,
      coord_precision == "10 km" ~ 10000,
      coord_precision == "Region" ~ 50000,
      TRUE ~ NA
    ),
    source = str_replace_all(source, c(
      "^Pascalis project Database.*$" = "PASCALIS Database",
      "^ATBI Mercantour Database.*$" = "ATBI Mercantour Database"
    ))
  ) |>
  group_by(longitude, latitude, coord_precision) |>
  # mutate(
  #   site_id = sprintf("EGCop_%d", cur_group_id()),
  # ) |>
  ungroup() |>
  mutate(
    order = order_FM,
    family = family_FM,
    genus = genus_FM,
    subgenus = subgenus_FM,
    specificEpithet = na_if(specificEpithet_FM, ""),
    infraspecificEpithet = infraspecificEpithet_FM,
    scientificName = str_trim(scientificName) |>
      str_replace("Nitocra", "Nitokra") |>
      str_replace("cf. ", "") |>
      str_replace("gr. hirta ", "") |>
      str_replace(" ?group .+$", "") |>
      str_replace_all(" s?sp\\.$", ""),
    acceptedNameUsage = acceptedNameUsage_FM,
    Locality = ifelse(str_detect(Locality, ".*[Ss]canned from map.*"), NA, Locality),
    publication = if_else(str_starts(source, "(Collection|Personal communication)"), NA, associatedReferences)
  ) |>
  mutate(
    scientificName = if_else(
      taxon_rank == "Subgenus", scientificName, str_replace_all(scientificName, " \\([^\\)]+\\) ", " ")
    ),
    collection = case_when(
      source == "Collection: F. Stoch " ~ "STOCH",
      source == "Collection: D. Galassi" ~ "GALASSI",
      TRUE ~ NA_character_
    ),
    source = if_else(
      str_starts(source, "(Literature|Collection:)"),
      NA,
      source
    )
  ) |>
  select(id = ID, everything(), -order_FM, -family_FM, -genus_FM, -subgenus_FM, -specificEpithet_FM, -infraspecificEpithet_FM, -scientificName_FM, -namePublishedInYear_FM, -Modif_taxonomy_FM, -scientificNameAuthorship_FM, -acceptedNameUsage_FM, -subfamily_FM, -associatedReferences, -researchGroup)

data |>
  select(source) |>
  distinct()
data

data <- data |>
  rename(
    site_name = Locality,
    taxon_name = scientificName,
    taxon_authorship = scientificNameAuthorship,
    verbatim_identification = acceptedNameUsage,
    identification_addendum = tax_id_addendum,
    coordinates_precision_m = coord_precision,
    sources = source,
    access_points = access_point,
    pub_year = PublicationYear,
    pub_verbatim = publication,
  ) |>
  mutate(
    identification_confer = case_when(
      tax_id_qualifier == "cf" ~ TRUE,
      TRUE ~ FALSE
    ),
    taxon_rank = case_when(
      taxon_name == "Ectinosomatidae" ~ "family",
      taxon_name == "Parapseudoleptomesochra subterranea" ~ "species",
      taxon_name == "Nitocrella hirta" ~ "species",
      taxon_name == "Speocyclops racovitzai" ~ "species",
      TRUE ~ taxon_rank
    ) |> str_to_lower(),
    collections = str_to_title(collection),
    taxon_name = taxon_name |>
      str_replace("Prosperpinicaris", "Proserpinicaris") |>
      str_replace("Kieferella", "Kieferiella"),
  ) |>
  select(-order, -family, -namePublishedInYear, -country, -collection, tax_id_qualifier)


data |>
  select(site_name) |>
  filter(str_detect(site_name, "\\?")) |>
  distinct() |>
  write_tsv("data/localities_with_question_mark.tsv")

dir.create(dirname(output_file), recursive = TRUE, showWarnings = FALSE)
write_tsv(data, output_file, na = "NA", quote = "needed")

message("Preprocessed Copepoda dataset written to ", output_file)
