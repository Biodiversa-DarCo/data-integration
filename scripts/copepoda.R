library(tidyverse)

data <- read_csv("data/Copepoda/Dataset_Copepoda.csv")


data <- data %>%
  mutate(
    habitat = case_when(
      habitat == "Several groundwater habitats" ~ "Groundwater",
      TRUE ~ habitat
    ),
    locationRemarks = case_when(
      locationRemarks == "hyporheic" ~ "Hyporheic zone",
      locationRemarks == "Hyporheic" ~ "Hyporheic zone",
      locationRemarks == "hyporheic habitat" ~ "Hyporheic zone",
      locationRemarks == "??" ~ NA,
      locationRemarks == "unknown" ~ NA,
      TRUE ~ locationRemarks
    ),
    Coord.Uncertainty = case_when(
      Coord.Uncertainty == "0.5 km" ~ "<1km",
      Coord.Uncertainty == "1 km" ~ "<1km",
      Coord.Uncertainty == "2 km" ~ "<10km",
      Coord.Uncertainty == "3 km" ~ "<10km",
      Coord.Uncertainty == "5 km" ~ "<10km",
      Coord.Uncertainty == "0.1 km" ~ "<100m",
      Coord.Uncertainty == "Catchment" ~ "<100m",
      Coord.Uncertainty == "20 km" ~ "10-100km",
      Coord.Uncertainty == "Comm.Centr" ~ "<100m",
      Coord.Uncertainty == "0.2 km" ~ "<1km",
      Coord.Uncertainty == "10 km" ~ "<10km",
      Coord.Uncertainty == "Region" ~ "10-100km",
      TRUE ~ NA
    )
  ) %>%
  mutate(
    locationRemarks = str_replace_all(locationRemarks, c(
      "cave" = "Cave",
      "well" = "Well",
      "wells" = "Well",
      "hyporhiec" = "Hyporheic",
      "different gw habitats" = "Groundwater",
      "usaturated" = "unsaturated"
    ))
  ) %>%
  group_by(decimalLongitude, decimalLatitude) %>%
  mutate(
    site_id = sprintf("Copepoda_%d", cur_group_id()),
  ) %>%
  ungroup()

data %>%
  select(Coord.Uncertainty) %>%
  distinct()

data %>%
  select(locationRemarks) %>%
  distinct() %>%
  arrange() %>%
  print(n = 400)
habitats <- data %>%
  select(locationRemarks, habitat) %>%
  distinct() %>%
  arrange() %>%
  print(n = 100)
