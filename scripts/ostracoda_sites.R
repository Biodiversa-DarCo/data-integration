library(tidyverse)
library(jsonlite)

countries = fromJSON("data/countries.json") %>%
  as_tibble() %>%
  mutate(Country = str_to_lower(name)) %>%
  select(Country, CountryCode = code)

# read_csv("data/countries.csv") %>%
#   mutate(Country = str_to_lower(Country_Name)) %>%
#   select(Country, CountryCode = Two_Letter_Country_Code)

data = read_tsv("data/Ostracoda/Dataset_Ostracoda_Natasa_Mori.tsv", col_names = T, quote = "\"", locale = locale(decimal_mark = ",")) %>%
  mutate(Country = str_to_lower(LocalityCountry)) %>%
  mutate(Country = case_when(
    Country == "russia" ~ "russian federation",
    Country == "moldova" ~ "moldova, republic of",
    Country == "north macedonia" ~ "macedonia",
    TRUE ~ Country
  )) %>%
  left_join(countries, by = "Country")

data %>%
  filter(is.na(CountryCode)) %>%
  select(Country)

(parsed = data %>%
  select(
    id, VerbLoc, LocID, Lat, Long, LatLongP, ElevMin, ElevMax,
    Country,
    CountryCode,
    Munici, Provin
  ) %>%
  mutate(
    VerbLoc = str_to_title(VerbLoc, locale = "en")
  ) %>%
  rename(
    name = VerbLoc,
    code = LocID,
    altitude = ElevMin
  ) %>%
  mutate(
    coordinates = pmap(list(Lat, Long, LatLongP), function(x, y, z) {
      list(
        latitude = x,
        longitude = y,
        precision = (
          switch(as.character(z),
            "0.001" = "<100m",
            "0.01" = "<1km",
            "0.1" = "<10km",
            "1" = "10-100km",
            "Unknown"
          )
        )
      )
    })
  ) %>%
  distinct(code, .keep_all = T) %>%
  select(
    id, name, code,
    country_code = CountryCode,
    coordinates,
    municipality = Munici,
    province = Provin
  )
)

parsed %>% filter(str_length(code) < 4)

# parsed$coordinates
# verblocs = parsed %>% select(id, VerbLoc)
# write_tsv(verblocs, "data/Aselloidea/verblocs.tsv")

dir.create("res/wad", showWarnings = F)
write_tsv(parsed, "res/wad/sites.tsv")
write_json(parsed, "res/wad/sites.json", pretty = T, digits = 10, auto_unbox = T)
