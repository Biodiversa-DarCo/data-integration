# %%
import pandas as pd

colNames = {
    "ID": "id",
    "decimalLongitude": "lon",
    "decimalLatitude": "lat",
    "Coord.Uncertainty": "precision",
    "PublicationYear": "year",
    "locationRemarks": "habitats",
    "acceptedNameUsage": "id_verbatim",
    "associatedReferences": "references",
}
columns = list(colNames.values())

rawData = pd.read_csv(
    "data/Copepoda/Dataset_Copepoda.csv",
    sep=",",
    decimal=".",
).rename(columns=colNames)[columns]

print(rawData)

# %%

rawData
