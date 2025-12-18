library(tidyverse)

output_dir <- "datasets/Ostracoda/res"

raw_data <- read_delim("datasets/Ostracoda/data/Dataset.csv", delim = ";")
raw_data %>%
  filter(!str_detect(family, "CC0")) %>%
  mutate(concat = str_squish(if_else(!is.na(genus), str_c(genus, species, sep = " "), family))) %>%
  filter(!str_starts(scientificName, concat)) %>%
  select(-concat) %>%
  write_tsv("datasets/Ostracoda/res/family_genus_species_check.tsv")


raw_data %>%
  filter(
    str_detect(verbatimIdentification, "aff\\.|cf") |
      str_detect(scientificName, "aff\\.|cf") |
      str_detect(Lineage, "aff|cf")
  ) %>%
  write_tsv("datasets/Ostracoda/res/aff_cf_check.tsv")

raw_data %>%
  group_by(decimalLatitude, decimalLongitude) %>%
  filter(length(unique(locality)) > 1) %>%
  arrange(decimalLatitude, decimalLongitude) %>%
  # select(ID, locality, decimalLatitude, decimalLongitude) %>%
  write_tsv(file.path(output_dir, "multiple_locality_same_coordinates.tsv"))

raw_data %>%
  group_by(locality) %>%
  filter(length(unique(decimalLatitude)) > 1 | length(unique(decimalLongitude)) > 1) %>%
  arrange(locality) %>%
  # select(ID, locality, decimalLatitude, decimalLongitude) %>%
  write_tsv(file.path(output_dir, "same_locality_multiple_coordinates.tsv"))
