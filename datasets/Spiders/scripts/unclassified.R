library(tidyverse)
library(argparse)


# Create parser
parser <- ArgumentParser(description = "Identify unclassified taxa in Spiders dataset")

# Add positional arguments
parser$add_argument("input",
  default = "datasets/Spiders/res/preprocessed.tsv",
  help = "Input TSV file"
)
parser$add_argument("output",
  default = "datasets/Spiders/res/unclassified_taxa.json",
  help = "Output TSV file"
)

print(commandArgs(trailingOnly = T))
# Parse arguments
if (length(commandArgs(trailingOnly = T)) > 0) {
  args <- parser$parse_args()
} else {
  args <- parser$parse_args(c("datasets/Spiders/res/preprocessed.tsv", "datasets/Spiders/res/unclassified_taxa.json"))
}

(
  data <- read_tsv(args$input) %>%
    filter(unclassified) %>%
    select(taxon_name, family, genus, taxon_rank) %>%
    distinct() %>%
    mutate(
      parent = genus,
      status = case_when(
        str_detect(taxon_name, "sp\\.") ~ "Unclassified",
        TRUE ~ "Unreferenced",
      ),
      taxon_rank = str_to_title(taxon_rank)
    )
)

data |>
  arrange(taxon_rank, family, genus) %>%
  rename(name = taxon_name, rank = taxon_rank) %>%
  select(-family, -genus) %>%
  jsonlite::write_json(
    path = args$output,
    pretty = TRUE,
    auto_unbox = TRUE
  )
