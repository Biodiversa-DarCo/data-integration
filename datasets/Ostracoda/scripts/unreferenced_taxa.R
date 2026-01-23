library(tidyverse)
library(argparse)


# Create parser
parser <- ArgumentParser(description = "Identify unreferenced taxa in Ostracoda dataset")

# Add positional arguments
parser$add_argument("input",
  default = "datasets/Ostracoda/data/missing_taxa.txt",
  help = "Input TSV file"
)
parser$add_argument("--preprocessed",
  default = "datasets/Ostracoda/res/Ostracoda.tsv",
  help = "Preprocessed TSV file"
)
parser$add_argument("output",
  default = "datasets/Ostracoda/res/unreferenced_taxa.json",
  help = "Output TSV file"
)

print(commandArgs(trailingOnly = T))
# Parse arguments
if (length(commandArgs(trailingOnly = T)) > 0) {
  args <- parser$parse_args()
} else {
  args <- parser$parse_args(c("datasets/Ostracoda/data/missing_taxa.txt", "datasets/Ostracoda/res/unreferenced_taxa.json"))
}

(
  preprocessed <- read_tsv(args$preprocessed) |>
    select(taxon_name, scientificNameAuthorship) |>
    rename(authorship = scientificNameAuthorship) |>
    distinct()
)

(
  data <- read_tsv(args$input, col_names = c("taxon_name")) |>
    mutate(
      rank = case_when(
        str_count(taxon_name, " ") == 0 ~ "Genus",
        str_count(taxon_name, " ") == 1 ~ "Species",
        TRUE ~ "Subspecies"
      ),
      status = "Unreferenced",
      parent = case_when(
        taxon_name == "Marmocandona" ~ "Candonidae",
        TRUE ~ str_remove(taxon_name, " [^ ]+$")
      )
    )
)

(
  data %>%
    arrange(rank, parent, taxon_name) %>%
    left_join(
      preprocessed,
      by = "taxon_name"
    ) %>%
    rename(name = taxon_name) %>%
    filter(
      !(name == "Marmocandona zschokkei" & authorship == "Wolf 1920"),
      !(name == "Mixtacandona botosaneanui" & authorship == "Danielopol 1973"),
      !(name == "Typhlocypris danubialis" & authorship == "Iepure et al. 2007"),
      !(name == "Typhlocypris eremita" & authorship == "Vejdovsky 1882"),
      !(name == "Typhlocypris marmonieri" & authorship == "Namiotko & Danielopol 2004"),
      !(name == "Cryptocandona kieferi danubialis" & authorship == "Namiotko et al. 2005")
    )
) %>%
  jsonlite::write_json(
    args$output,
    pretty = TRUE,
    auto_unbox = TRUE,
    na = "null"
  )
