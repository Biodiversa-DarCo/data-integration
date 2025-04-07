library(tidyverse)

rawData = read_tsv(
  "data/Aselloidea/Aselloidea_All_Occurences_Europe_DarCo_For_Louis.tsv",
  col_names = T, quote = "\"", locale = locale(decimal_mark = ",")
)

persons = c(
  "ZAGMAJSTER M" = c(first_name = "Maja", last_name = "Zagmajster", organisation = "Uni-Lj"), # "Zagmajster Maja",
  "MALARD F" = c(first_name = "Florian", last_name = "Malard", organisation = "LEHNA"),
  "MORI N" = c(first_name = "Nataša", last_name = "Mori", organisation = "NIB"),
  "LEFEBURE T" = c(first_name = "Tristan", last_name = "Lefebure", organisation = "LEHNA"),
  "DELIC T" = c(first_name = "Teo", last_name = "Delić", organisation = "Uni-Lj"),
  "DOUADY C" = c(first_name = "Christophe", last_name = "Douady", organisation = "LEHNA"),
  "SACLIER N" = c(first_name = "Natanaëlle", last_name = "Saclier", organisation = "LEHNA"),
  "CREUZE DES CHATELLIERS M" = c(first_name = "Michel", last_name = "Creuzé des Châtelliers", organisation = "LEHNA"),
  "MERMILLOD BLONDIN F" = c(first_name = "Florian", last_name = "Mermillod-Blondin", organisation = "LEHNA"),
  "FRANCOIS C" = c(first_name = "Clémentine", last_name = "François", organisation = "LEHNA")
)

with_access_point = function(habitat, access_point) {
  added_habitat = dplyr::case_when(
    access_point == "Well" ~ list(c("Aquatic", "Subsurface", "Freshwater")),
    (access_point %in% c("Wash house", "Fountain")) ~ list(c("Aquatic", "Freshwater")),
    (access_point %in% c("Lake", "Marsh", "Pond")) ~ list(c("Aquatic", "Surface", "Lentic")),
    (access_point == "River") ~ list(c("Aquatic", "Surface", "Freshwater", "Lotic")),
    (access_point %in% c("Stream", "Spring")) ~ list(c("Aquatic", "Freshwater", "Lotic")),
    (access_point %in% c("Canal", "Aqueduct")) ~ list(c("Aquatic", "Freshwater")),
    (access_point %in% c("Cave", "Tunnel", "Mine")) ~ list(c("Subsurface")),
    access_point == "Water catchment" ~ list(c("Aquatic", "Freshwater")),
    access_point == "Hyporheic zone" ~ list(c("Aquatic", "Hyporheic zone", "Aquifer", "Subsurface")),
    TRUE ~ list(c("Aquatic"))
  )
  union(habitat[[1]], added_habitat[[1]])
}

data = rawData %>%
  select(
    rowID,
    site_code = LocID,
    lat = Lat,
    lon = Long,
    precision = LatLongP,
    altitude = ElevMin,
    site_comments = LocRem,
    event_date = EventDate,
    event_participants = CollBy,
    habitats = Habita,
    access_points = Access,
    sampling_effort = SamplEff,
    sampling_method = SamplMet,
    fixative = Fixative,
    sampling_program = Program,
    sampling_target = Target,
    sampling_comments = EventRem,
    temperature = WaterTemp,
    conductivity = WaterCond,
    id_date = DateIden,
    id_curator = IdenBy,
    id_criterion = IdenAttri,
    id_verbatim = IdenVer,
    MOTU,
    occurrence_code = OccID,
    occurrence_type = BasRec,
    reported_by = RefBy,
    organism_quantity = OrgQuan,
    organism_count = OrgCount,
    occurrence_comments = OccRem,
    references = AssRef,
    gene = Gene,
    accession_number = AN,
    specimen_voucher = Isolate,
    original_taxon_name = Origin_tax_name,
    collection = Collection,
    original_link = OriginalLink,
    data_source = DataSource,
  ) %>%
  mutate(

    # convert habitats
    habitats = case_when(
      habitats == "0 - INCONNU" ~ list(c()),
      habitats == "AQUIFERE ALLUVIAL" ~ list(c("Aquatic", "Subsurface", "Aquifer", "Alluvial")),
      habitats == "AQUIFERE FISSURE" ~ list(c("Aquatic", "Subsurface", "Aquifer", "Fissured")),
      habitats == "AQUIFERE KARSTIQUE" ~ list(c("Aquatic", "Subsurface", "Aquifer", "Karst")),
      habitats == "AQUIFERE POREUX" ~ list(c("Aquatic", "Subsurface", "Aquifer", "Porous")),
      habitats == "EAU DOUCE DE SURFACE" ~ list(c("Surface", "Aquatic", "Freshwater")),
      habitats == "EAU DOUCE SOUTERRAINE" ~ list(c("Subsurface", "Aquatic", "Freshwater")),
      habitats == "EAU SALEE SOUTERRAINE" ~ list(c("Subsurface", "Aquatic", "Saltwater")),
      habitats == "SYSTEME LENTIQUE" ~ list(c("Aquatic", "Lentic")),
      habitats == "SYSTEME LOTIQUE" ~ list(c("Aquatic", "Lotic")),
      habitats == "ZONE HYPORHEIQUE" | access_points == "ZONE HYPORHEIQUE" ~ list(c("Aquatic", "Subsurface", "Aquifer", "Hyporheic zone")),
      habitats == "ZONE NON SATUREE KARSTIQUE" ~ list(c("Aquatic", "Subsurface", "Aquifer", "Karst", "Unsaturated")),
      habitats == "ZONE SATUREE KARSTIQUE" ~ list(c("Aquatic", "Subsurface", "Aquifer", "Karst", "Saturated")),
      TRUE ~ list(c())
    ),
    access_points = case_when(
      access_points == "0 - INCONNU" ~ NA,
      access_points == "AUTRE" ~ NA,
      access_points == "ZONE HYPORHEIQUE" ~ "Hyporheic zone",
      access_points == "AQUEDUC" ~ "Aqueduct",
      access_points == "CANAL" ~ "Canal",
      access_points == "CAPTAGE EAU" ~ "Water catchment",
      access_points == "ETANG" ~ "Pond",
      access_points == "FONTAINE" ~ "Fountain",
      access_points == "GROTTE" ~ "Cave",
      access_points == "LAC" ~ "Lake",
      access_points == "LAVOIR" ~ "Wash house",
      access_points == "MARAIS MARE" ~ "Marsh",
      access_points == "MINE" ~ "Mine",
      access_points == "PUITS" ~ "Well",
      access_points == "RIVIERE" ~ "River",
      access_points == "RUISSEAU" ~ "Stream",
      access_points == "SOURCE" ~ "Spring",
      access_points == "TUNNEL" ~ "Tunnel",
      TRUE ~ NA
    ),
    habitats_from_access_points = map2(
      habitats, access_points,
      ~ with_access_point(.x, .y)
    ),
    habitats = map2(
      habitats, habitats_from_access_points,
      ~ union(.x, .y)
    ),
  )


data %>% mutate(
  event_participants = event_participants %>% map(~ {
    print(.x)
    print(str_split(.x, "\\|", simplify = T))
    str_split(.x, "\\|", simplify = T) %>%
      map_dfr(function(x) {
        p <- list_c(persons[x])
        print(p)
        if (is.null(p)) {
          name = name %>%
            str_to_title() %>%
            str_split_i(" ", -1)
          return(tibble_row(
            first_name = str_trim(name[1]),
            last_name = str_trim(name[2]),
            organisation = NA_character_
          ))
        } else {
          print(p)
          return(tibble_row(!!!list_c(p)))
        }
      })
  }),
)




data %>%
  select(habitats, access_points, habitats_from_access_points) %>%
  distinct() %>%
  mutate(
    habitats = map(habitats, ~ paste(.x, collapse = ", ")) %>% unlist(),
    habitats_from_access_points = map(habitats_from_access_points, ~ paste(.x, collapse = ", ")) %>% unlist(),
  ) %>%
  arrange(habitats) %>%
  print(n = 100)

data %>%
  select(event_participants) %>%
  mutate(participants = map(event_participants, ~ paste(.x, collapse = ", ")) %>% unlist()) %>%
  select(participants) %>%
  distinct()

# data %>%
#   select(access_points) %>%
#   distinct() %>%
#   arrange(access_points)
