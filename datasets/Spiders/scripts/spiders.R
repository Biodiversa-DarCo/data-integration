library(tidyverse)

data <- read_tsv("datasets/Spiders/res/preprocessed.tsv", locale = locale(decimal_mark = "."))

spiders <- data |>
    mutate(row_id = row_number()) |>
    select(
        site_name = site_name,
        locality = locality,
        latitude = latitude,
        longitude = longitude,
        coordinates_precision_m = coord_precision,
        event_date = sampling_date,
        access_points,
        habitats = habitat,
        occurrence_comments,
        taxon_name,
        taxon_rank,
        content_description,
        identified_by,
        identification_confer = tax_id_confer,
        specimen_quantity,
        sources = collection,
        pub_verbatim,
        pub_doi = pub_DOI,
        pub_authors,
        pub_year,
        pub_title,
        pub_journal
    ) |>
    mutate(
        sources = str_replace_all(sources, " & ", "|"),
        taxon_rank = str_to_lower(taxon_rank),
        taxon_name = str_squish(taxon_name),
    )

bad_ranks <- data |>
    select(taxon_name, taxon_rank) |>
    distinct() |>
    group_by(taxon_name) |>
    summarise(count = n()) |>
    filter(count > 1)

fixed_ranks <- bad_ranks |>
    select(taxon_name) |>
    mutate(taxon_rank = case_when(
        str_count(taxon_name, " ") == 1 ~ "species",
        str_count(taxon_name, " ") == 2 ~ "subspecies",
        TRUE ~ "genus"
    ))

spiders <- spiders |> rows_update(fixed_ranks, by = "taxon_name")

(bib <- data |>
    select(
        row_number = row_id,
        pub_verbatim,
        pub_doi = pub_DOI,
        pub_authors,
        pub_year,
        pub_title,
        pub_journal
    ) |>
    filter(!is.na(pub_doi) | !is.na(pub_verbatim)) |>
    separate_longer_delim(
        cols = -row_number,
        delim = "|"
    ) |>
    mutate(across(-row_number, trimws)) |>
    rename_with(~ str_replace_all(., "pub_", ""))
)

bib |> write_tsv("datasets/Spiders/res/bibliography.tsv", quote = "needed")

spiders |>
    select(-pub_verbatim, -pub_doi, -pub_authors, -pub_year, -pub_title, -pub_journal) |>
    write_tsv("datasets/Spiders/res/spiders.tsv", quote = "needed")
