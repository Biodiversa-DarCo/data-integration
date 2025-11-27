library(tidyverse)

args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 2) {
  stop("Usage: preprocessing.R <input_file.tsv> <output_file.tsv>")
}
input_file <- args[1]
output_file <- args[2]

data <- read_tsv(input_file) %>%
  # remove NA columns
  select(where(~ !all(is.na(.)))) %>%
  mutate(
    row_id = row_number(),
    # FIXME cannot generate site codes until the site duplicates situation is resolved
    # site_code = str_c("SPIDERS_", row_id),
    latitude = round(latitude, 5),
    longitude = round(longitude, 5),
    tax_id_confer = str_detect(taxon_name, "cf\\."),
    unclassified = unclassified & (!tax_id_confer) & (!str_detect(taxon_name, "sp\\.$")),
    habitat = case_when(
      access_points %in% c("Cave", "Artificial gallery") ~ str_c(habitat, "Subterranean", sep = ","),
      access_points == "Shallow Subterranean Habitats (SSH)" ~ str_c(habitat, "Shallow subterraean habitat (SSH)", sep = ","),
    )
  ) %>%
  relocate(row_id)
data

data %>% write_tsv(output_file)
