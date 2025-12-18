library(tidyverse)

raw_data <- read_delim("datasets/Ostracoda/data/Dataset.csv", delim = ";")
(
  data <- read_delim("datasets/Ostracoda/data/Dataset.csv", delim = ";") %>%
    select(-geodeticDatum, -TaxonID) %>%
    mutate(
      taxonRank = str_to_title(taxonRank),
      id_confer = str_detect(verbatimIdentification, "cf"),
      # After checking, only Typhlocypris cf. eremita is concerned with confer id
      species = if_else(id_confer, "eremita", species),
      scientificNameAuthorship = scientificNameAuthorship %>% stringi::stri_trans_general("Latin-ASCII") %>% str_remove_all("\\,"),
      taxon_name = verbatimIdentification %>%
        stringi::stri_trans_general("Latin-ASCII") %>%
        str_remove_all("\\,") %>%
        str_remove_all(scientificNameAuthorship) %>%
        str_remove_all("\\(\\)") %>%
        str_remove_all("\\(?([A-Z][a-z]+([A-Z][a-z]+\\,)* ?)*([A-Z][a-z]+ ?\\& ?)* ?[A-Z][a-z]+ [0-9]{4}\\)?") %>%
        str_remove("((ge)?n\\. *)?sp\\.? *$") %>%
        str_squish(),
      taxon_name = if_else(id_confer, "Typhlocypris eremita", taxon_name),
      unclassified = str_detect(verbatimIdentification, "gen\\.|sp\\. ?[^$ ]|aff\\."),
    )
)

raw_data %>%
  filter(scientificName != verbatimIdentification)
distinct() %>%
  nrow()

filter(ID == 1145) %>%
  print(n = 100)
filter(str_detect(decimalLatitude, "CC0") | is.na(decimalLatitude))

select(taxon_name, unclassified, id_confer) %>%
  distinct() %>%
  print(n = 200)
