library(tidyverse)
library(argparse)

# Create parser
parser <- ArgumentParser(description = "Preprocess Ostracoda dataset")

# Add positional arguments
parser$add_argument("input",
  default = "datasets/Ostracoda/data/Dataset.tsv",
  help = "Input TSV file"
)
parser$add_argument("output",
  default = "datasets/Ostracoda/res/preprocessed.tsv",
  help = "Output TSV file"
)

# Add optional arguments
parser$add_argument("--taxonomy-fix",
  default = "datasets/Ostracoda/data/taxonomy_fix.tsv",
  help = "Taxonomy fix TSV file [default: %(default)s]"
)
parser$add_argument("--aff-cf-fix",
  default = "datasets/Ostracoda/data/aff_cf.tsv",
  help = "Aff/cf fix TSV file [default: %(default)s]"
)
parser$add_argument("--habitats",
  default = "datasets/Ostracoda/data/habitats.tsv",
  help = "Habitat access TSV file [default: %(default)s]"
)
parser$add_argument("--gbif",
  default = "datasets/Ostracoda/data/GBIF_censor_recovery.tsv",
  help = "GBIF censor recovery TSV file [default: %(default)s]"
)
parser$add_argument("--missing-coords",
  default = "datasets/Ostracoda/data/coordinates_recovery.tsv",
  help = "Missing coordinates recovery TSV file [default: %(default)s]"
)
print(commandArgs(trailingOnly = T))
# Parse arguments
if (length(commandArgs(trailingOnly = T)) > 0) {
  args <- parser$parse_args()
} else {
  args <- parser$parse_args(c("datasets/Ostracoda/data/Dataset.tsv", "datasets/Ostracoda/res/preprocessed.tsv"))
}

input_file <- args$input
output_file <- args$output
taxonomy_fix_file <- args$taxonomy_fix
aff_cf_fix_file <- args$aff_cf_fix
habitats_file <- args$habitats
gbif_file <- args$gbif
missing_coords_file <- args$missing_coords

MISSING_COORDS_DELETE <- c(
  1114,
  1116,
  1118,
  1130,
  1162,
  1163,
  1164,
  1361,
  1386,
  1390,
  1395,
  1418,
  1428,
  1448,
  1449
)

(
  taxonomy_fix <- read_tsv(taxonomy_fix_file, locale = locale(decimal_mark = ",")) %>%
    mutate(
      unclassified = is.na(Classified) | !Classified,
      id_confer = str_detect(Lineage, "cf\\."),
      taxonRank = str_to_title(taxonRank)
    ) %>%
    select(ID, family, genus, species, scientificNameAuthorship, unclassified, taxonRank, Lineage, id_confer, scientificName)
)

(
  aff_cf_fix <- read_tsv(aff_cf_fix_file) %>%
    mutate(
      id_confer = str_detect(Lineage, "cf\\."),
    ) %>%
    select(ID, family, genus, species, scientificNameAuthorship, taxonRank, Lineage, id_confer, scientificName)
)

(
  habitats <- read_tsv(habitats_file) %>%
    select(ID, habitat, access_points)
)

(gbif_records <- read_tsv(gbif_file, locale = locale(decimal_mark = ",")) %>%
  select(-Rights, -`Input.into.DB.-.name`, -SourceType) %>%
  rename(
    site_name = "LocalityName",
    altitude = "Altitude",
    scientificNameAuthorship = "authorship",
  ) %>%
  mutate(scientificName = taxon_name)
)

missing_coords <- read_tsv(missing_coords_file)

(
  # Dataset.tsv is manually fixed version of Dataset.csv where line break in record 1469 was removed.
  data <- read_tsv(input_file, locale = locale(decimal_mark = ",")) %>%
    # dedup strictly identical records
    # ignore ID when applying distinct
    distinct_at(vars(-ID), .keep_all = TRUE) %>%
    filter(!str_detect(family, "CC0")) %>% # drop censored GBIF records
    mutate(
      latitude = round(parse_double(decimalLatitude, locale = locale(decimal_mark = ",")), 5),
      longitude = round(parse_double(decimalLongitude, locale = locale(decimal_mark = ",")), 5),
      altitude = round(parse_double(elevationInMeters, locale = locale(decimal_mark = ",")), 2),
    ) %>%
    select(-geodeticDatum, -TaxonID, -decimalLatitude, -decimalLongitude, -elevationInMeters) %>%
    mutate(
      id_confer = str_detect(verbatimIdentification, "cf"),
    ) %>%
    left_join(taxonomy_fix, by = "ID", suffix = c(".old", ".new")) %>%
    mutate(
      family = coalesce(family.new, family.old),
      genus = coalesce(genus.new, genus.old),
      species = coalesce(species.new, species.old),
      scientificNameAuthorship = coalesce(scientificNameAuthorship.new, scientificNameAuthorship.old),
      scientificName = coalesce(scientificName.new, scientificName.old),
      taxonRank = coalesce(taxonRank.new, taxonRank.old),
      Lineage = coalesce(Lineage.new, Lineage.old),
      id_confer = coalesce(id_confer.new, id_confer.old)
    ) %>%
    # drop .old columns
    select_at(vars(-ends_with(".old"), -ends_with(".new"))) %>%
    left_join(aff_cf_fix, by = "ID", suffix = c(".old", ".new")) %>%
    mutate(
      family = coalesce(family.new, family.old),
      genus = coalesce(genus.new, genus.old),
      species = coalesce(species.new, species.old),
      scientificNameAuthorship = coalesce(scientificNameAuthorship.new, scientificNameAuthorship.old),
      scientificName = coalesce(scientificName.new, scientificName.old),
      taxonRank = coalesce(taxonRank.new, taxonRank.old),
      Lineage = coalesce(Lineage.new, Lineage.old),
      id_confer = coalesce(id_confer.new, id_confer.old),
    ) %>%
    # drop .old and .new columns
    select_at(vars(-ends_with(".old"), -ends_with(".new"))) %>%
    select(-verticalDatum, -locationID, -`Input.into.DB.-.name`, -rightsHolder) %>%
    rename(
      site_name = locality,
      sampling_date = dateIdentified,
      data_repository = basisOfRecord,
      taxon_rank = taxonRank,
      verbatim_identification = verbatimIdentification,
    ) %>%
    mutate(
      # After checking, only Typhlocypris cf. eremita is concerned with confer id
      scientificNameAuthorship = scientificNameAuthorship %>% stringi::stri_trans_general("Latin-ASCII") %>% str_remove_all("\\,"),
      taxon_name = scientificName %>%
        stringi::stri_trans_general("Latin-ASCII") %>%
        str_remove_all("\\,") %>%
        str_remove_all(scientificNameAuthorship) %>%
        str_remove_all("\\(\\)") %>%
        str_remove_all("\\(?([A-Z][a-z]+([A-Z][a-z]+\\,)* ?)*([A-Z][a-z]+ ?\\& ?)* ?[A-Z][a-z]+ [0-9]{4}\\)?") %>%
        str_remove("((ge)?n\\. *)?sp\\.? *$") %>%
        str_squish(),
    ) %>%
    bind_rows(
      .,
      filter(., ID == 706) %>%
        mutate(
          species = "danielopoli",
          scientificName = "Schellencandona danielopoli Issartel & Marmonier, 2025",
          taxon_name = "Schellencandona danielopoli",
          scientificNameAuthorship = "Issartel & Marmonier, 2025",
        ),
      filter(., ID == 676) %>%
        mutate(
          species = "n. sp. J4",
          unclassified = TRUE,
          scientificName = "Schellencandona sp. J4, 2006",
          verbatim_identification = "Schellencandona sp. J4, 2006",
          taxon_name = "Schellencandona n. sp. J4",
          scientificNameAuthorship = NA,
        ),
      gbif_records
    ) %>%
    mutate(
      references = if_else(
        ID %in% seq(706, 717),
        "Issartel, C., & Marmonier, P. (2025). Description of five new species of Schellencandona Meisch, 1996 (Ostracoda: Candoninae) from the southern French Alps, a highly diversified area for groundwater ostracods. European Journal of Taxonomy, 1022(1), 85–133. https://doi.org/10.5852/ejt.2025.1022.3083",
        references
      ),
      # taxon_name = if_else(id_confer, "Typhlocypris eremita", taxon_name) %>% str_remove("Namiotko et al. 2005$"),
      # species = if_else(id_confer, "eremita", species),
      unclassified = case_when(
        taxon_name %in% c("Mixtacandona juberthieae", "Schellencandona malardi", "Schellencandona danielopoli", "Pseudolimnocythere") ~ FALSE,
        TRUE ~ if_else(unclassified, unclassified, str_detect(verbatim_identification, "gen\\.|sp\\. ?[^$ ]|aff\\."))
      ),
      id_addendum = case_when(
        str_detect(Lineage, "cf\\.") ~ NA,
        TRUE ~ Lineage,
      ),
      taxon_rank = str_to_title(taxon_rank),
      references = str_replace_all(references, "", "è") %>%
        str_replace_all("eè", "è") %>%
        str_replace_all("franais", "français") %>%
        str_replace_all("dâun", "d'un") %>%
        str_replace_all("karstiqueÊ", "karstique ") %>%
        str_replace_all("Universityy", "University ") %>%
        str_replace_all("\\\"\"E. Boegan\\\"\"", "\"E. Boegan\"") %>%
        str_replace("^Unpubl. data P. ", "Unpublished Data: P. "),
      data_repository = case_when(
        str_starts(data_repository, "Pascalis") ~ "PASCALIS",
        str_starts(data_repository, "ATBI") ~ data_repository,
        str_starts(data_repository, "NODE") ~ "NODE (Nonmarine Ostracod Distribution in Europe), David J. Horne (ed.)",
        str_starts(data_repository, "SubBio") ~ "SubBioDB",
        str_starts(data_repository, "Literature|River|") ~ NA,
        TRUE ~ data_repository
      ),
      # correction from Pierre cf. missing_coordinates.xlsx
      genus = case_when(
        ID == 1394 ~ "Mixtacandona",
        TRUE ~ genus
      ),
      sampling_date = str_replace_all(sampling_date, "\\.", "/"),
      identifiedBy = case_when(
        identifiedBy == "PASCALIS" ~ NA_character_,
        identifiedBy == "FM" ~ "Marrone, F.",
        identifiedBy == "GR" ~ "Rossetti, G.",
        identifiedBy == "D. Taliana" ~ "Taliana, D.",
        identifiedBy == "F. Stoch" ~ "Stoch, F.",
        identifiedBy == "Fabio Zanicelli" ~ "Zanicelli, F.",
        identifiedBy == "Nataša Mori" ~ "Mori, N.",
        TRUE ~ identifiedBy
      ) %>% str_replace_all(";", "|"),
      datasetName = case_when(
        # not a dataset but a paper
        str_starts(datasetName, "Revision") ~ NA,
        str_starts(datasetName, "Freshwater ostracods") ~ NA,
        str_starts(datasetName, "A preliminary") ~ NA,
        str_starts(datasetName, "An annotated") ~ NA,
        str_starts(datasetName, "Checklist and") ~ NA,
        str_starts(datasetName, "Diversity of") ~ NA,
        TRUE ~ datasetName
      )
    ) %>%
    select(-habitat, -access_points, -locationRemarks, -Lineage) %>%
    left_join(habitats, by = "ID") %>%
    mutate(
      occurrence_comments = case_when(
        references %in% c(
          "Unpublished Data: University of Vienna",
          "PersonalCommunication_NationalparkGesäuse",
          "Unpublished Data: P. Marmonier",
          "Karanovic I. pers com to Maja Zagmajster",
          "Unpublished Data: C. Bou et Michel Caillon: Albi: France"
        ) ~ references,
        TRUE ~ NA_character_
      ),
      doi = str_extract(references, "doi(\\.org\\/|:)?(10.*$)", group = 2),
      references = if_else(is.na(doi) & !(references %in% c(
        "Unpublished Data: University of Vienna",
        "PersonalCommunication_NationalparkGesäuse",
        "Unpublished Data: P. Marmonier",
        "Karanovic I. pers com to Maja Zagmajster",
        "Unpublished Data: C. Bou et Michel Caillon: Albi: France"
      )), references, NA_character_),
      taxon_name = str_remove(taxon_name, " \\([^\\)]+\\)$| [A-Za-z]+, [0-9]{4}$| Namiotko et al. 2005$"),
    ) %>%
    filter(!ID %in% MISSING_COORDS_DELETE) %>%
    # replace missing coordinates, overwriting columns latitude and longitude
    left_join(missing_coords, by = "ID", suffix = c(".old", ".new")) %>%
    mutate(
      latitude = coalesce(latitude.new, latitude.old),
      longitude = coalesce(longitude.new, longitude.old),
      coord_precision = coalesce(coord_precision.new, coord_precision.old),
    ) %>%
    select_at(vars(-ends_with(".old"), -ends_with(".new"))) %>%
    mutate(
      site_name = if_else(str_length(site_name) <= 3, str_c("Ostracoda_", site_name), site_name),
      coord_precision = if_else(is.na(coord_precision), "Unknown", coord_precision)
    ) %>%
    relocate(
      ID, verbatim_identification, scientificName, taxon_name, class, order, family, genus, species, id_confer, id_addendum,
      data_repository, everything()
    )
) %>%
  write_tsv(output_file)


# (
#   dups <- data %>%
#     group_by(site_name, latitude, longitude, taxon_name, sampling_date) %>%
#     summarise(n = n()) %>%
#     filter(n > 1)
# )


# data %>%
#   select(data_repository, datasetName, informationWithheld) %>%
#   distinct()
# # transform each to a concatenated string
# (dup_strings <- dups %>%
#   mutate(
#     dup_string = paste(site_name, latitude, longitude, taxon_name, sampling_date, sep = " | ")
#   ) %>%
#   pull(dup_string)
# )

# data %>%
#   mutate(dups = paste(site_name, latitude, longitude, taxon_name, sampling_date, sep = " | ")) %>%
#   filter(dups %in% dup_strings) %>%
#   arrange(dups) %>%
#   write_tsv("datasets/Ostracoda/res/duplicates.tsv")
