library(tidyverse)

args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 3) {
  stop("Usage: Rscript unreferenced_taxa.R <input_file> <missing_taxa_file> <output_file>")
}

dataset_file <- args[1]
missing_taxa_file <- args[2]
output_file <- args[3]

missing_taxa = read_tsv(missing_taxa_file, col_names = c("name")) %>%
  mutate(status = if_else(str_detect(name, "sp\\. "), "Unclassified", "Unreferenced"))

dataset = read_tsv(dataset_file)


new_taxa = dataset %>%
  select(scientificName, taxon_rank, genus, specificEpithet, family, scientificNameAuthorship) %>%
  distinct() %>%
  inner_join(missing_taxa, by = c("scientificName" = "name")) %>%
  mutate(
    parent = case_when(
      taxon_rank == "Subspecies" ~ str_c(genus, specificEpithet, sep = " "),
      taxon_rank == "Species" ~ genus,
      taxon_rank == "Genus" ~ family,
      TRUE ~ NA_character_
    )
  ) %>%
  select(
    name = scientificName,
    parent,
    status,
    authorship = scientificNameAuthorship,
    rank = taxon_rank
  )

(new_genuses = dataset %>%
  filter(str_detect(genus, "gen.")) %>%
  select(name = genus, parent = family, authorship = scientificNameAuthorship) %>%
  distinct() %>%
  mutate(rank = "Genus", status = "Unclassified") %>%
  add_row(name = "Kieferella", parent = "Cyclopidae", rank = "Genus", status = "Unreferenced") %>%
  add_row(name = "Entzicaris", parent = "Parastenocarididae", rank = "Genus", status = "Unreferenced", authorship = "Jakobi, 1972") %>%
  add_row(name = "Acanthocyclops stammeri", parent = "Acanthocyclops", rank = "Species", status = "Unreferenced", authorship = "Kiefer, 1930")
)

bind_rows(new_genuses, new_taxa) %>%
  jsonlite::write_json(output_file, auto_unbox = TRUE, pretty = TRUE)
