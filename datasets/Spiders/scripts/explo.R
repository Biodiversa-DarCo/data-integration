library(tidyverse)


args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 2) {
  stop("Usage: preprocessing.R <input_file.tsv> <output_file.tsv>")
}
input_file <- args[1]
output_dir <- args[2]

dir.create(output_dir, showWarnings = FALSE, recursive = TRUE)

# data <- read_tsv("datasets/Spiders/data/template_spiders_db.tsv") %>%
data <- read_tsv(input_file) %>%
  mutate(
    row_number = row_number(),
    latitude = round(latitude, 5),
    longitude = round(longitude, 5)
  ) %>%
  relocate(row_number)

# data %>%
#   select(collection) %>%
#   distinct() %>%
#   write_tsv(file.path(output_dir, "collections.tsv"))


data %>%
  group_by(latitude, longitude) %>%
  filter(length(unique(site_name)) > 1 & !is.na(site_name)) %>%
  arrange(latitude, longitude, site_name) %>%
  write_tsv(file.path(output_dir, "sites_duplicated_coordinates.tsv"))


data %>%
  filter(is.na(latitude) | is.na(longitude)) %>%
  write_tsv(file.path(output_dir, "sites_missing_coordinates.tsv"))

data %>%
  filter(str_detect(site_name, "\\?\\w")) %>%
  write_tsv(file.path(output_dir, "bad_encoding_candidates.tsv"))

data %>%
  filter(unclassified & !str_detect(taxon_name, "cf\\.|sp\\.$")) %>%
  write_tsv(file.path(output_dir, "unclassified.tsv"))


data %>%
  group_by(site_name) %>%
  filter((
    length(unique(latitude)) > 1 | length(unique(longitude)) > 1
  ) & !is.na(site_name)) %>%
  arrange(site_name) %>%
  write_tsv(file.path(output_dir, "sites_multiple_coordinates.tsv"))
