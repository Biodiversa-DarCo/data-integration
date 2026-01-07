library(tidyverse)
library(argparse)

parser = ArgumentParser()

parser$add_argument("input_file", help = "Path to the input data file")
parser$add_argument("output_file", help = "Path to the output duplicates data file")

if (length(commandArgs(trailingOnly = T)) > 0) {
  args <- parser$parse_args()
} else {
  args <- parser$parse_args(
    c("datasets/Austria/data/dataset.tsv", "datasets/Austria/res/duplicates.tsv")
  )
}

(
  data <- read_tsv(args$input_file) %>%
    # drop last column
    select(-"...53") %>%
    mutate(
      row_id = row_number(),
      latitude = round(latitude, 5),
      longitude = round(longitude, 5)
    )
)
(
  dups <- data %>%
    filter(paste0(site_name, taxon_name, sampling_date) %in% paste0(dups$site_name, dups$taxon_name, dups$sampling_date)) %>%
    select(!starts_with("pub")) %>%
    # change order of columns
    relocate(row_id, site_name, latitude, longitude, sampling_date, taxon_name, occurrence_id, specimen_quantity, content_description, occurrence_comments, seq_comments, everything())
) |>
  write_tsv(args$output_file)
