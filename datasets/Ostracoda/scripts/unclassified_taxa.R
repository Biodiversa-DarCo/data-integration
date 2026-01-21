library(tidyverse)
library(argparse)


# Create parser
parser <- ArgumentParser(description = "Identify unclassified taxa in Ostracoda dataset")

# Add positional arguments
parser$add_argument("input",
  default = "datasets/Ostracoda/res/preprocessed.tsv",
  help = "Input TSV file"
)
parser$add_argument("output",
  default = "datasets/Ostracoda/res/unclassified_taxa.json",
  help = "Output TSV file"
)

print(commandArgs(trailingOnly = T))
# Parse arguments
if (length(commandArgs(trailingOnly = T)) > 0) {
  args <- parser$parse_args()
} else {
  args <- parser$parse_args(c("datasets/Ostracoda/res/preprocessed.tsv", "datasets/Ostracoda/res/unclassified_taxa.json"))
}

(
  data = read_tsv(args$input) %>%
    filter(unclassified) %>%
    select(taxon_name, family, genus, species, taxon_rank) %>%
    distinct() %>%
    mutate(
      parent = case_when(
        str_starts(genus, "gen\\. ") ~ str_c(family, genus, sep = " "),
        TRUE ~ genus,
      ),
      status = case_when(
        str_detect(taxon_name, "n\\. sp\\.") ~ "Unclassified",
        TRUE ~ "Unreferenced",
      )
    )
)

# print(data, n=100)

(
  new_genera = data %>%
    filter(str_starts(genus, "gen\\. ")) %>%
    mutate(
      species = NA,
      taxon_rank = "Genus",
      taxon_name = str_c(family, genus, sep = " "),
      parent = family,
    )
)

bind_rows(data, new_genera) %>%
  arrange(taxon_rank, family, genus, species) %>%
  rename(name = taxon_name, rank = taxon_rank) %>%
  select(-family, -genus, -species) %>%
  jsonlite::write_json(
    path = args$output,
    pretty = TRUE,
    auto_unbox = TRUE
  )
