library(tidyverse)
library(jsonlite)

data = read_delim("data/references.csv", delim = ";", col_names = T, quote = "\"")
parsed = data %>%
  select(1:3) %>%
  rename(
    code = "Code source",
    year = "Année source",
    verbatim = "Libellé source",
  ) %>%
  mutate(
    authors = str_replace_all(verbatim, " ?\\(?[0-9]{4}.*", ""),
    journal = str_replace(verbatim, "[_\\.0-9:\\-, \\(\\)p\\?\\/\\–]*\\.*$", "") %>%
      str_split("\\. ?") %>%
      sapply(
        FUN = last
      ),
    title = str_replace(verbatim, fixed(authors), "") %>%
      str_replace(fixed(year), "") %>%
      str_replace("^[ \\.]+", "") %>%
      str_replace(if_else(
        journal == "",
        fixed("no journal provided : ignore"), # actually has no effect
        fixed(journal)
      ), "") %>%
      str_replace(" ?\\.? ?[ 0-9\\-()\\,\\:]+\\.*$", "")
  )

parsed %>%
  filter(str_detect(authors, "Garcia")) %>%
  select(journal)

write_tsv(parsed, "res/references.tsv")
write_json(parsed, "res/references.json", pretty = T)
