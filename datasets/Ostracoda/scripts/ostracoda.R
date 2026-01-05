library(tidyverse)
library(argparse)

# Create parser
parser <- ArgumentParser(description = "Process Ostracoda dataset")

# Add positional arguments
parser$add_argument("input",
  default = "datasets/Ostracoda/data/Dataset.tsv",
  help = "Input TSV file")
parser$add_argument("output",
  default = "datasets/Ostracoda/res/preprocessed.tsv",
  help = "Output TSV file")

# Add optional arguments
parser$add_argument("--taxonomy-fix",
                    default = "datasets/Ostracoda/data/taxonomy_fix.tsv",
                    help = "Taxonomy fix TSV file [default: %(default)s]")
parser$add_argument("--aff-cf-fix",
                    default = "datasets/Ostracoda/data/aff_cf.tsv",
                    help = "Aff/cf fix TSV file [default: %(default)s]")
parser$add_argument("--habitats",
                    default = "datasets/Ostracoda/data/habitats.tsv",
                    help = "Habitat access TSV file [default: %(default)s]")

# Parse arguments
args <- parser$parse_args()

input_file <- args$input
output_file <- args$output
taxonomy_fix_file <- args$taxonomy_fix
aff_cf_fix_file <- args$aff_cf_fix
habitats_file <- args$habitats


(
  taxonomy_fix = read_tsv(taxonomy_fix_file) %>%
    mutate(
      unclassified = is.na(Classified) | !Classified,
      id_confer = str_detect(Lineage, "cf\\."),
      taxonRank = str_to_title(taxonRank)
    ) %>%
    select(ID, family, genus, species, scientificNameAuthorship, unclassified, taxonRank, Lineage, id_confer, scientificName)
)

(
  aff_cf_fix = read_tsv(aff_cf_fix_file) %>%
    mutate(
      id_confer = str_detect(Lineage, "cf\\."),
    ) %>%
    select(ID, family, genus, species, scientificNameAuthorship, taxonRank, Lineage, id_confer, scientificName)
)

(
  habitats = read_tsv(habitats_file) %>%
    select(ID, habitat, access_points)
)




(
  # Dataset.tsv is manually fixed version of Dataset.csv where line break in record 1469 was removed.
  data <- read_tsv(input_file) %>%
    select(-geodeticDatum, -TaxonID) %>%
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
      id_confer = coalesce(id_confer.new, id_confer.old),
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
    mutate(
      references = if_else(
        ID %in% seq(706, 717),
        "Issartel, C., & Marmonier, P. (2025). Description of five new species of Schellencandona Meisch, 1996 (Ostracoda: Candoninae) from the southern French Alps, a highly diversified area for groundwater ostracods. European Journal of Taxonomy, 1022(1), 85–133. https://doi.org/10.5852/ejt.2025.1022.3083",
        references
      ),
      taxonRank = str_to_title(taxonRank),
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
      # taxon_name = if_else(id_confer, "Typhlocypris eremita", taxon_name) %>% str_remove("Namiotko et al. 2005$"),
      # species = if_else(id_confer, "eremita", species),
      unclassified = if_else(unclassified, unclassified, str_detect(verbatimIdentification, "gen\\.|sp\\. ?[^$ ]|aff\\.")),
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
          verbatimIdentification = "Schellencandona sp. J4, 2006",
          taxon_name = "Schellencandona n. sp. J4",
          scientificNameAuthorship = NA,
        )
    ) %>%
    filter(!str_detect(family, "CC0")) %>%
    mutate(
      references = str_replace_all(references, "", "è") %>%
        str_replace_all("eè", "è") %>%
        str_replace_all("franais", "français") %>%
        str_replace_all("dâun", "d'un") %>%
        str_replace_all("karstiqueÊ", "karstique ") %>%
        str_replace_all("Universityy", "University ") %>%
        str_replace_all("\\\"\"E. Boegan\\\"\"", "\"E. Boegan\"") %>%
        str_replace("^Unpubl. data P. ", "Unpublished Data: P. "),
      data_repository = case_when(
        str_starts(basisOfRecord, "Pascalis") ~ "PASCALIS",
        str_starts(basisOfRecord, "ATBI") ~ basisOfRecord,
        str_starts(basisOfRecord, "NODE") ~ "NODE (Nonmarine Ostracod Distribution in Europe), David J. Horne (ed.)",
        str_starts(basisOfRecord, "SubBio") ~ "SubBioDB",
      )
    ) %>%
    select(-habitat, -locationRemarks) %>%
    left_join(habitats, by = "ID") %>%
    relocate(ID, verbatimIdentification, scientificName, taxon_name, class, order, family, genus, species, everything())
) %>%
  write_tsv(output_file)

