library(tidyverse)

args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 2) {
  stop("Usage: recover_encoding.R <input_file.tsv> <fixed_encoding.csv> <output_file.tsv>")
}
input_file <- args[1]
fixed_encoding_file <- args[2]
output_file <- args[3]

dataset <- read_tsv(input_file)
fixed_encoding <- read_csv(fixed_encoding_file)

merged <- dataset %>%
  left_join(fixed_encoding, by = "ID", suffix = c("", "_fixed")) %>%
  mutate(
    Locality = ifelse(!is.na(Locality_fixed), Locality_fixed, Locality),
    scientificNameAuthorship = ifelse(!is.na(scientificNameAuthorship_fixed), scientificNameAuthorship_fixed, scientificNameAuthorship),
    associatedReferences = ifelse(!is.na(associatedReferences_fixed), associatedReferences_fixed, associatedReferences)
  ) %>%
  select(-ends_with("_fixed"))

dir.create(dirname(output_file), recursive = TRUE, showWarnings = FALSE)
write_tsv(merged, output_file, na = "NA")
