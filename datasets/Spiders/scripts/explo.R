library(tidyverse)

dir.create("datasets/Spiders/res/", showWarnings = FALSE)

data = read_tsv("datasets/Spiders/data/template_spiders_db.tsv")

data %>%
  group_by(latitude, longitude) %>%
  filter(length(unique(site_name)) > 1) %>%
  arrange(latitude, longitude) %>%
  write_tsv("datasets/Spiders/res/sites_duplicated_coordinates.tsv")


data %>%
  filter(is.na(latitude) | is.na(longitude)) %>%
  write_tsv("datasets/Spiders/res/sites_missing_coordinates.tsv")

data %>%
  filter(str_detect(site_name, "\\?\\w")) %>%
  write_tsv("datasets/Spiders/res/bad_encoding_candidates.tsv")

data %>%
  filter(unclassified & !str_detect(taxon_name, "cf\\.|sp\\.$")) %>%
  write_tsv("datasets/Spiders/res/unclassified.tsv")
