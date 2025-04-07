library(tidyverse)


data = read_tsv("data/Aselloidea/Aselloidea_All_Occurences_Europe_DarCo_For_Louis.tsv", col_names = T, quote = "\"", locale = locale(decimal_mark = ","))


pb_dates = data %>%
  select(
    event_date = EventDate, biomat_code = OccID
  ) %>%
  filter(event_date == "01/06/2013") %>%
  mutate(sampling_code = str_extract(biomat_code, "\\|([0-9A-Z]+_[0-9]+)") %>% str_remove("\\|"))

pb_dates %>% write_tsv("res/wad/problematic_dates.tsv")
