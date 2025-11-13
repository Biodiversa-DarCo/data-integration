library(tidyverse)

args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 2) {
  stop("Usage: extract_broken_lines <input_file.csv> <output_file.tsv>")
}
input_file <- args[1]
output_file <- args[2]


data <- read_csv(input_file)
broken_lines = data %>%
  select(ID, Locality, scientificNameAuthorship, Coord.Validator, associatedReferences) %>%
  filter(
    str_detect(Locality, "�") | str_detect(associatedReferences, "�") |
      str_detect(scientificNameAuthorship, "[^éèöa-zA-Z0-9,& ().\\-]")
  )

write_tsv(broken_lines, output_file)
