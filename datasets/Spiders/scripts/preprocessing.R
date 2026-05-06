library(tidyverse)
library(argparse)

parser <- ArgumentParser()

parser$add_argument("input_file", help = "Path to the input data file")
parser$add_argument("output_file", help = "Path to the output preprocessed data file")
parser$add_argument("--encoding-fix",
  help = "Path to the file with fixed site names",
  default = "datasets/Spiders/data/patches/encoding_fix.tsv"
)
parser$add_argument("--multiple-coordinates-fix",
  help = "Path to the file with fixed coordinates for sites with multiple coordinates",
  default = "datasets/Spiders/data/patches/multiple_coordinates_fix.tsv"
)
parser$add_argument("--multiple-site-names-fix",
  help = "Path to the file with fixed site names for sites with multiple names",
  default = "datasets/Spiders/data/patches/multiple_site_names_fix.tsv"
)

if (length(commandArgs(trailingOnly = T)) > 0) {
  args <- parser$parse_args()
} else {
  args <- parser$parse_args(
    c("datasets/Spiders/data/spiders_db.tsv", "datasets/Spiders/res/preprocessed.tsv")
  )
}

print(args)

data <- read_tsv(args$input_file, locale = locale(decimal_mark = ",")) |>
  # remove NA columns except content_description
  select(where(~ !all(is.na(.)))) |>
  mutate(across(where(is.character), ~ str_trim(.))) |>
  mutate(
    row_id = row_number(),
    # FIXME cannot generate site codes until the site duplicates situation is resolved
    # site_code = str_c("SPIDERS_", row_id),
    latitude = round(latitude, 5),
    longitude = round(longitude, 5),
    tax_id_confer = str_detect(taxon_name, "cf\\."),
    unclassified = unclassified & (!tax_id_confer) & (!str_detect(taxon_name, "sp\\.$")),
    habitat = case_when(
      access_points %in% c("Cave", "Artificial gallery") ~ str_c(habitat, "Subterranean", sep = ","),
      TRUE ~ habitat,
    ),
    content_description = NA_character_
  ) |>
  relocate(row_id)

# --------------------------------------------------------
# Encoding fix
# --------------------------------------------------------

encoding_fix <- read_tsv(args$encoding_fix, show_col_types = FALSE) |>
  select(row_number, site_name)

data <- data |>
  left_join(encoding_fix, by = c("row_id" = "row_number")) |>
  mutate(site_name = coalesce(site_name.y, site_name.x)) |>
  select(-site_name.x, -site_name.y) |>
  relocate(row_id, site_name)

message("Encoding fix applied")

# ---------------------------------------------------------
# Multiple coordinates fix
# ---------------------------------------------------------

coordinates_fix <- read_tsv(args$multiple_coordinates_fix, show_col_types = FALSE) |>
  select(row_number, latitude, longitude)

data <- data |>
  left_join(coordinates_fix, by = c("row_id" = "row_number")) |>
  mutate(
    latitude = coalesce(latitude.y, latitude.x),
    longitude = coalesce(longitude.y, longitude.x)
  ) |>
  select(-latitude.x, -latitude.y, -longitude.x, -longitude.y)

message("Multiple coordinates fix applied")

# ---------------------------------------------------------
# Multiple site names fix
# ---------------------------------------------------------

names_fix <- read_tsv(args$multiple_site_names_fix, show_col_types = FALSE) |>
  select(row_number, site_name)

data <- data |>
  left_join(names_fix, by = c("row_id" = "row_number")) |>
  mutate(site_name = coalesce(site_name.y, site_name.x)) |>
  select(-site_name.x, -site_name.y)


data <- data |> relocate(row_id, site_name, latitude, longitude)

message("Multiple site names fix applied")


data <- data |>
  mutate(
    coord_precision = case_when(
      is.na(coord_precision) ~ NA_character_,
      coord_precision <= 100 ~ "<100m",
      coord_precision <= 1000 ~ "<1km",
      coord_precision <= 10000 ~ "<10km",
      TRUE ~ "10-100km"
    )
  )

# ---------------------------------------------------------
# General fixes
# ---------------------------------------------------------

data |>
  group_by(site_name, latitude, longitude) |>
  filter(length(unique(coord_precision)) > 1) |>
  select(site_name, latitude, longitude, coord_precision) |>
  arrange(site_name) |>
  print(n = Inf)

message("Fix sites with multiple coordinate precision values")
data <- data |>
  # for each site, use the predominant coordinate precision, if there are multiple records with different precision
  group_by(site_name, latitude, longitude) |>
  mutate(
    coord_precision = {
      non_missing_precision <- na.omit(coord_precision)

      if (
        n_distinct(coord_precision, na.rm = FALSE) > 1 &&
          length(non_missing_precision) > 0
      ) {
        names(sort(table(non_missing_precision), decreasing = TRUE))[1]
      } else {
        first(coord_precision)
      }
    }
  ) |>
  ungroup()

message("Fix site names")
omisalj_patch = tibble(
  row_id = 27826,
  site_name = "Under the rock near Omišalj, Krk island a cave near Draga Bašćanska",
  coord_precision = "<1km",
  sampling_date = "1929-09-16",
  content_description = "1 male, 1 juvenile female",
  specimen_quantity = 2,
)

print(names(data))

data = data |>
  mutate(site_name = case_when(
    str_starts(site_name, "Agios Georgios, 50m,") ~ "Agios Georgios",
    str_starts(site_name, "Exo Mouliana, along path to Richtis Waterfall") ~ "Exo Mouliana, along path to Richtis Waterfall",
    str_starts(site_name, "Cetina") ~ "Cetina (“Cajetina”)",
    TRUE ~ site_name
  )) |>
  rows_update(omisalj_patch, by = "row_id")



data |>
  mutate(s = str_length(site_name)) |>
  filter(s > 100) |>
  distinct() |>
  select(row_id, site_name, s) |>
  print(n = Inf)


data <- data |>
  mutate(
    pub_DOI = str_remove(pub_DOI, "^https?://doi\\.org/"),
    sampling_date = if_else(
      str_detect(sampling_date, "^\\d{4}(-\\d{2}(-\\d{2})?)?$"),
      sampling_date,
      str_remove(sampling_date, "\\/.*$"),
    ) |> replace_na(""),
    id_confer = str_detect(taxon_name, "cf\\.") |> na_if(FALSE),
    taxon_name = (
      str_remove(taxon_name, "sp\\.\\s*$") |> 
      str_remove("cf\\.\\s*") |> 
      str_remove(" ?NA *$") |> 
      str_trim()
    ),
    taxon_name = case_when(
        taxon_name == "Spermphora senoculata" ~ "Spermophora senoculata",
        taxon_name == "Tegenaria vel Malthonica" ~ "Tegenaria",
        taxon_name == "Hoplopholcus sululin" ~ "Hoplopholcus suluin",
        taxon_name == "Rugathodes bellicosum" ~ "Rugathodes bellicosus",
        taxon_name == "Centromerus corsica" ~ "Centromerus corsicus",
        taxon_name == "Folkia subcupresa" ~ "Folkia subcupressa",
        taxon_name == "Carpathonesticus carpathicus" ~ "Carpathonesticus carpaticus",
        taxon_name == "Troglohyphantes brignoli" ~ "Troglohyphantes brignolii",
        taxon_name == "Rugathodes bellicosum" ~ "Rugathodes bellicosus",
        taxon_name == "Leptoneta cryticola" ~ "Leptoneta crypticola",
        taxon_name == "Metallina merianae" ~ "Metellina merianae",
        taxon_name == "Metopobractus cavernicola" ~ "Metopobactrus cavernicola",
        taxon_name == "Meta vel Metellina" ~ "Meta",
        taxon_name == "Clubiona cicur" ~ "Cicurina cicur",
        taxon_name == "Palliduphantes leprosus" ~ "Lepthyphantes leprosus",
        taxon_name == "Palliduphants spelaeorum" ~ "Palliduphantes spelaeorum",
        taxon_name == "Robertus cardensensis" ~ "Robertus cardesensis",
        taxon_name == "Hoplopholcus gazipasta" ~ "Hoplopholcus gazipasa",
        taxon_name == "Coelotes jurinitschi" ~ "Inermocoelotes jurinitschi",
        TRUE ~ taxon_name
      )
  ) |>
  filter(!(taxon_name %in% c("Amaurobius vel Coelotes", "NA NA"))) |>
  # repair wrong separators for one pub verbatim 
  mutate(
    pub_verbatim = case_when(
      row_id == 24755 ~ "Pavlek, M., & Ozimec, R. (2009). New cave-dwelling species of genus Troglohyphantes (Araneae, Linyphiidae) for Croatian fauna. Natura Craotica, 18(1), 29–37. | Mammola, S., Cardoso, P., Angyal, D., Balázs, G., Blick, T., Brustel, H., … Isaia, M. (2019). Continental data on cave-dwelling spider communities across Europe (Arachnida: Araneae). Biodiversity Data Journal, 7. https://doi.org/10.3897/BDJ.7.e38492 | Jalžić, B. & Rnjak, G. 2019: Glogova jama na Sniježnici. Subterranea Croatica, 17, 2, 44-50.",
      TRUE ~ pub_verbatim    
    ) |> str_replace_all("\\s*\\|\\s*", "|"),
    # fix missing publication years for records with multiple publications, using the years from pub_verbatim
    pub_year = case_when(
      row_id == 1097 ~ str_flatten(c("2010", "2019"), collapse = "|"),
      row_id == 6186 ~ str_flatten(c("2018", "NA"), collapse = "|"),
      row_id == 6187 ~ str_flatten(c("2022", "2022"), collapse = "|"),
      row_id == 8085 ~ str_flatten(c("2018", "2022"), collapse = "|"),
      row_id == 9870 ~ str_flatten(c("2010", "2019"), collapse = "|"),
      row_id == 9871 ~ str_flatten(c("2010", "2019"), collapse = "|"),
      row_id == 24755 ~ str_flatten(c("2009", "2019", "2019"), collapse = "|"),
      row_id == 24756 ~ str_flatten(c("2009", "2019"), collapse = "|"),
      row_id == 24757 ~ str_flatten(c("2009", "2019"), collapse = "|"),
      TRUE ~ as.character(pub_year)
    ) |> str_replace_all("\\s*\\|\\s*", "|"),
    pub_DOI = (
      str_replace_all(pub_DOI, "\\s*\\|\\s*", "|") |> 
      # fix typo in DOI
      str_replace("10.1002/mmnz.1971047020", "10.1002/mmnz.19710470203")
    ),
    pub_year = str_replace_all(pub_year, "\\s*\\|\\s*", "|"),
    pub_authors = str_replace_all(pub_authors, "\\s*\\|\\s*", "|"),
    pub_title = str_replace_all(pub_title, "\\s*\\|\\s*", "|"),
    pub_journal = str_replace_all(pub_journal, "\\s*\\|\\s*", "|")
  ) |>
  filter(!is.na(latitude) & !is.na(longitude) & !is.na(taxon_name) & taxon_name != "NA")


# add coordinate-based suffix for duplicated site names with different coordinates
data <- data |>
  group_by(site_name) |>
  mutate(
    .coord_key = str_c(latitude, longitude, sep = "|"),
    .coord_suffix = dense_rank(.coord_key),
    .coord_count = n_distinct(.coord_key)
  ) |>
  ungroup() |>
  mutate(site_name = if_else(.coord_count > 1, str_c(site_name, " [", .coord_suffix, "]"), site_name)) |>
  select(-.coord_key, -.coord_suffix, -.coord_count)



# ---------------------------------------------------------
# Write output
# ---------------------------------------------------------
message("Writing output to file: ", args$output_file)
data |>
  distinct() |>
  write_tsv(args$output_file, quote = "needed")
