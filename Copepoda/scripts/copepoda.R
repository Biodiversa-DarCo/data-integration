library(tidyverse)

args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 2) {
  stop("Usage: copepoda.R <input_file.tsv> <output_file.tsv>")
}
input_file <- args[1]
output_file <- args[2]

data <- read_tsv(input_file, na = c("NULL", "Unclear", "unclear", "??", "?", "Unknown")) %>%
  mutate(
    Modif_taxonomy_FM = ifelse(Modif_taxonomy_FM == "yes", T, F),
    taxon_rank = case_when(
      !is.na(infraspecificEpithet) ~ "Subspecies",
      !is.na(specificEpithet) & specificEpithet != "sp." ~ "Species",
      !is.na(subgenus) ~ "Subgenus",
      TRUE ~ "Genus"
    ),
  ) %>%
  select(-habitat, -locationRemarks, -geodeticDatum, -Easting_EPSG3035, -Northing_EPSG3035, -Coord.Validator) %>%
  rename(
    habitat = Habitat_Florian,
    access_point = Access_Florian,
    longitude = decimalLongitude,
    latitude = decimalLatitude,
    coord_precision = Coord.Uncertainty,
    tax_id_qualifier = FM_dwc_identificationQualifier,
    tax_id_addendum = FM_identification_addendum
  ) %>%
  mutate(
    coord_precision = case_when(
      coord_precision == "0.5 km" ~ "<1km",
      coord_precision == "1 km" ~ "<1km",
      coord_precision == "2 km" ~ "<1km",
      coord_precision == "3 km" ~ "<10km",
      coord_precision == "5 km" ~ "<10km",
      coord_precision == "0.1 km" ~ "<100m",
      coord_precision == "Catchment" ~ "10-100km",
      coord_precision == "20 km" ~ "10-100km",
      coord_precision == "Comm.Centr" ~ "<10km",
      coord_precision == "0.2 km" ~ "<100m",
      coord_precision == "10 km" ~ "<10km",
      coord_precision == "Region" ~ "10-100km",
      TRUE ~ NA
    ),
    source = str_replace_all(source, c(
      "^Pascalis project Database.*$" = "PASCALIS Database",
      "^ATBI Mercantour Database.*$" = "ATBI Mercantour Database"
    ))
  ) %>%
  group_by(longitude, latitude, coord_precision) %>%
  mutate(
    site_id = sprintf("EGCop_%d", cur_group_id()),
  ) %>%
  ungroup() %>%
  mutate(
    order = order_FM,
    family = family_FM,
    genus = genus_FM,
    subgenus = subgenus_FM,
    specificEpithet = na_if(specificEpithet_FM, ""),
    infraspecificEpithet = infraspecificEpithet_FM,
    scientificName = str_trim(scientificName_FM) %>%
      str_replace_all(" s?sp\\.$", "") %>%
      str_replace_all(" \\([^\\)]+\\) ", " ") %>%
      str_replace("Nitocra", "Nitokra"),
    acceptedNameUsage = acceptedNameUsage_FM,
    Locality = ifelse(str_detect(Locality, ".*[Ss]canned from map.*"), NA, Locality)
  ) %>%
  select(id = ID, site_id, everything(), -order_FM, -family_FM, -genus_FM, -subgenus_FM, -specificEpithet_FM, -infraspecificEpithet_FM, -scientificName_FM, -namePublishedInYear_FM, -Modif_taxonomy_FM, -scientificNameAuthorship_FM, -acceptedNameUsage_FM, -subfamily_FM)

data %>%
  select(family) %>%
  distinct() %>%
  pull(family)

data

dir.create(dirname(output_file), recursive = TRUE, showWarnings = FALSE)
write_tsv(data, output_file, na = "NA")
