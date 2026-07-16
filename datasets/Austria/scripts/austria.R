library(tidyverse)

(
  data <- read_tsv("datasets/Austria/res/preprocessed.tsv", quote = "\"") |>
    mutate(
      row_number = row_number(),
      country = "AUT",
      coordinates_precision_m = case_when(
        coord_precision == "<100m" ~ 100,
        coord_precision == "<1km" ~ 1000,
        coord_precision == "<10km" ~ 10000,
        TRUE ~ NA_real_
      ),
      content_description = case_when(
        str_starts(occurrence_comments, "[0-9]") ~ occurrence_comments,
        TRUE ~ NA_character_
      ),
      occurrence_comments = case_when(
        str_starts(occurrence_comments, "[0-9]") ~ NA_character_,
        TRUE ~ occurrence_comments
      ),
      sampling_date = if_else(
        is.na(sampling_date),
        NA_character_,
        purrr::map_chr(
          str_split(sampling_date, "/"),
          ~ str_c(rev(.x), collapse = "-")
        )
      ),
      taxon_rank = case_when(
        str_detect(taxon_name, "^[A-Z][a-z]+ [a-z]+ [a-z]+$") ~ "Subspecies",
        str_detect(taxon_name, "^[A-Z][a-z]+ [a-z]+$") ~ "Species",
        str_detect(taxon_name, "^[A-Z][a-z]+$") ~ "Genus",
        TRUE ~ NA_character_
      )
    ) |>
    select(
      row_number,
      #   sampling_id
      #   site_code
      site_name,
      locality = site_comments,
      country,
      latitude,
      longitude,
      coordinates_precision_m,
      #   altitude
      event_date = sampling_date,
      sampling_participants,
      #   duration
      access_points,
      habitats = habitat,
      # sampling_targets
      sampling_methods,
      #   sampling_fixatives
      sampling_comments,
      occurrence_code = occurrence_id,
      type_status,
      occurrence_comments,
      taxon_name,
      taxon_rank,
      # taxon_authorship,
      # verbatim_identification,
      # identified_by,
      # identification_date
      # identification_confer
      # identification_addendum
      content_description,
      specimen_quantity,
      pub_authors,
      pub_year,
      pub_title,
      pub_journal,
      pub_verbatim,
      pub_DOI,
      sources = collection
    )
)

data |>
  write_tsv("datasets/Austria/res/batch_austria.tsv", quote = "needed")
