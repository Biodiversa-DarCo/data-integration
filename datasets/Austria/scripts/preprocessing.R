library(tidyverse)
library(argparse)

parser = ArgumentParser()

parser$add_argument("input_file", help = "Path to the input data file")
parser$add_argument("output_file", help = "Path to the output preprocessed data file")

if (length(commandArgs(trailingOnly = T)) > 0) {
  args <- parser$parse_args()
} else {
  args <- parser$parse_args(
    c("datasets/Austria/data/dataset.tsv", "datasets/Austria/res/preprocessed.tsv")
  )
}
(
  data <- read_tsv(args$input_file, locale = locale(decimal_mark = ",")) |>
    select(-"...53") |>
    mutate(
      latitude = round(latitude, 5),
      longitude = round(longitude, 5)
    )
)

(
  jstor_records = data |>
    filter(str_detect(pub_DOI, "www.jstor.org")) |>
    mutate(
      pub_authors = "Strouhal, Hans",
      pub_year = 1958,
      pub_title = "Asellus (Proasellus) im nördlichen Österreich (Isopoda, Asellota)",
      pub_journal = "Annalen des Naturhistorischen Museums in Wien"
    )
)

merge_occurrences = function(data, ids_to_merge, quantity = NA_integer_, comments = NA_character_, verbatim_id = NA_character_) {
  to_merge = filter(data, occurrence_id %in% ids_to_merge)
  sequence_data = to_merge |>
    filter(!is.na(seq_comments)) |>
    select(occurrence_id, seq_comments) |>
    group_by(occurrence_id) |>
    group_modify(~ {
      seq_tibble = str_remove(.x$seq_comments, "^GenBank_Accession_") |>
        str_split("_", simplify = T) |>
        as.vector() |>
        map_dfr(function(x) {
          tibble(
            accession = str_remove(x, "\\(.*\\)$"),
            gene = str_remove_all(str_extract(x, "\\(.*\\)$"), "[\\(\\)]"),
            seq_specimen_identifier = .y$occurrence_id
          )
        })
      seq_tibble
    }) |>
    ungroup()
  print(sequence_data)
  data |>
    filter(!(occurrence_id %in% ids_to_merge)) |>
    bind_rows(
      to_merge |>
        slice(1) |>
        mutate(
          occurrence_id = paste(ids_to_merge, collapse = "_"),
          specimen_quantity = if_else(is.na(quantity), sum(to_merge$specimen_quantity), quantity),
          occurrence_comments = comments,
          seq_comments = NA_character_,
          verbatim_identification = if_else(is.na(verbatim_id), verbatim_identification, verbatim_id)
        ) |>
        uncount(nrow(sequence_data)) |>
        mutate(
          accession_number = sequence_data$accession,
          gene = sequence_data$gene,
          seq_specimen_identifier = sequence_data$seq_specimen_identifier
        )
    )
}

(
  res <- data |>
    filter(!(occurrence_id %in% c("STYA1445", "STYA1442"))) |>
    merge_occurrences(c("STYA1438", "STYA1439", "STYA1440")) |>
    #     filter(occurrence_id == "STYA1438_STYA1439_STYA1440") |>
    #     select(seq_specimen_identifier, occurrence_id, gene, accession, seq_comments, specimen_quantity)
    #  )
    merge_occurrences(c("STYA1411", "STYA1414"), comments = "3 females, 1 juvenile") |>
    merge_occurrences(c("STYA1498", "STYA1499")) |>
    merge_occurrences(c("STYA1472", "STYA1473")) |>
    merge_occurrences(c("STYA1422", "STYA1425"), comments = "19 females, 30 juveniles") |>
    merge_occurrences(c("STYA1351", "STYA1352", "STYA1353", "STYA1443")) |>
    merge_occurrences(c("STYA1360", "STYA1444")) |>
    merge_occurrences(c("STYA1354", "STYA1355", "STYA1356")) |>
    merge_occurrences(c("STYA1361", "STYA1451")) |>
    merge_occurrences(c("STYA1474", "STYA1475")) |>
    merge_occurrences(c("STYA1434", "STYA1435")) |>
    merge_occurrences(c("STYA1357", "STYA1358", "STYA1426")) |>
    merge_occurrences(c("STYA1372", "STYA1373", "STYA1380")) |>
    merge_occurrences(c("STYA1374", "STYA1381")) |>
    merge_occurrences(c("STYA1375", "STYA1382")) |>
    merge_occurrences(c("STYA1377", "STYA1383"), verbatim_id = "P. strouhali strouhali") |>
    merge_occurrences(c("STYA1436", "STYA1437")) |>
    merge_occurrences(c("STYA1398", "STYA1399")) |>
    merge_occurrences(c("STYA1261", "STYA1452")) |>
    merge_occurrences(c("STYA1465", "STYA1487")) |>
    merge_occurrences(c("STYA1347", "STYA1362", "STYA1363"), verbatim_id = "P. strouhali") |>
    merge_occurrences(c("STYA1348", "STYA1349", "STYA1350")) |>
    # All records from WAD are already in the Asellidae dataset, except for one
    filter(is.na(collection) | str_detect(collection, "PROASELLUS_SP|LAHAU_200703")) |>
    # Repair jstor records
    filter(!str_detect(pub_DOI, "www.jstor.org")) |>
    bind_rows(jstor_records)
) |>
  write_tsv(args$output_file)
