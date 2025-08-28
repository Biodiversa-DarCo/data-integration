# EGCop: an expert-curated occurrence dataset of European groundwater-dwelling copepods (Crustacea: Copepoda)


## Description of the data and file structure

The dataset (named "EGCop") contains about 7,000 occurrence records of groundwater-dwelling copepods, located across the European continent. Records were retrieved both from literature spanning the 1907 – 2017 period and from recent international research projects focusing on groundwater biodiversity (e.g., PASCALIS, AQUALIFE, DarCo Biodiversa+). Each record was attentively scrutinized by senior researchers specialized into the taxonomy and biogeography of freshwater copepods, to provide correct identification of specimens according to the latest advances in copepods’ systematics. Further, spatial uncertainty was estimated for the geographic coordinates of each record, provided at 0.001-degree resolution (~100 m), by coupling in-depth web searches about specimens’ sampling localities with georeferencing GIS techniques. Information about the habitat characterizing the sampling localities is also provided for most records.

Names of most columns in the dataset, which is provided in two different formats (.csv and .xlsx), follow the Darwin Core standard to make data easily interpretable and reusable.

In both the file formats, we labelled "NULL" the cells for which no information was available with respect to a certain variable (e.g., "habitat" column filled with NULL when the habitat where the species was sampled is unknown). We also labelled "NULL" the cells where a certain variable was not applicable to the considered records (e.g., "subgenus" column filled with NULL when the taxonomy of the relevant species does not include a subgeneric taxon).

### Files and variables

#### File: EGCop\_nov2024.xlsx

**Description:** EGCop dataset provided in XLSX format.

##### Variables

* ID: numeric identifier of the single records.
* order: "dwc:order" ([http://rs.tdwg.org/dwc/terms/order)](http://rs.tdwg.org/dwc/terms/order)
* family: "dwc:family" ([http://rs.tdwg.org/dwc/terms/family)](http://rs.tdwg.org/dwc/terms/family)
* subfamily: "dwc:subfamily" ([http://rs.tdwg.org/dwc/terms/subfamily](http://rs.tdwg.org/dwc/terms/subfamily))
* genus: "dwc:genus" ([http://rs.tdwg.org/dwc/terms/genus](http://rs.tdwg.org/dwc/terms/genus))
* subgenus: "dwc:subgenus" ([http://rs.tdwg.org/dwc/terms/subgenus](http://rs.tdwg.org/dwc/terms/subgenus))
* specificEpithet: "dwc:specificEpithet" ([http://rs.tdwg.org/dwc/terms/specificEpithet](http://rs.tdwg.org/dwc/terms/specificEpithet))
* infraspecificEpithet: "dwc:infraspecificEpithet" ([http://rs.tdwg.org/dwc/terms/infraspecificEpithet](http://rs.tdwg.org/dwc/terms/infraspecificEpithet))
* scientificName: "dwc:scientificName" ([http://rs.tdwg.org/dwc/terms/scientificName](http://rs.tdwg.org/dwc/terms/scientificName))
* scientificNameAuthorship: "dwc:scientificNameAuthorship" ([http://rs.tdwg.org/dwc/terms/scientificNameAuthorship](http://rs.tdwg.org/dwc/terms/scientificNameAuthorship))
* acceptedNameUsage: "dwc:acceptedNameUsage" ([http://rs.tdwg.org/dwc/terms/acceptedNameUsage](http://rs.tdwg.org/dwc/terms/acceptedNameUsage))
* namePublishedInYear: "dwc:namePublishedInYear" ([http://rs.tdwg.org/dwc/terms/namePublishedInYear](http://rs.tdwg.org/dwc/terms/namePublishedInYear))
* country: "dwc:country"  ([http://rs.tdwg.org/dwc/terms/country](http://rs.tdwg.org/dwc/terms/country))
* Locality: "dwc:locality" ([http://rs.tdwg.org/dwc/terms/locality](http://rs.tdwg.org/dwc/terms/locality))
* locationRemarks: "dwc:locationRemarks" ([http://rs.tdwg.org/dwc/terms/locationRemarks](http://rs.tdwg.org/dwc/terms/locationRemarks))
* habitat: "dwc:habitat" ([http://rs.tdwg.org/dwc/terms/habitat](http://rs.tdwg.org/dwc/terms/habitat))
* decimalLongitude: "dwc:decimalLongitude" ([http://rs.tdwg.org/dwc/terms/decimalLongitude](http://rs.tdwg.org/dwc/terms/decimalLongitude))
* decimalLatitude: "dwc:decimalLatitude" ([http://rs.tdwg.org/dwc/terms/decimalLatitude](http://rs.tdwg.org/dwc/terms/decimalLatitude))
* geodeticDatum: "dwc:geodeticDatum" ([http://rs.tdwg.org/dwc/terms/geodeticDatum](http://rs.tdwg.org/dwc/terms/geodeticDatum))
* Easting_EPSG3035: easting coordinates in ETRS89-extended / LAEA Europe (EPSG: 3035) projected coordinate system.
* Northing_EPSG3035: northing coordinates in ETRS89-extended / LAEA Europe (EPSG: 3035) projected coordinate system.
* Coord.Uncertainty: spatial uncertainty in the provided coordinates (spanning from 0.1 km to "Region").
* Coord.Validator: person who performed the assessment of the spatial uncertainty of records' coordinates.
* associatedReferences: "dwc:associatedReferences" ([http://rs.tdwg.org/dwc/terms/associatedReferences](http://rs.tdwg.org/dwc/terms/associatedReferences))
* source: literature, personal collection or research project from which the single records were obatained.
* researchGroup: researchers involved in the project during which the single records were collected.

#### File: EGCop\_nov2024.csv

**Description:** EGCop dataset provded in CSV format.

##### Variables

* ID: numeric identifier of the single records.
* order: "dwc:order" ([http://rs.tdwg.org/dwc/terms/order)](http://rs.tdwg.org/dwc/terms/order)
* family: "dwc:family" ([http://rs.tdwg.org/dwc/terms/family)](http://rs.tdwg.org/dwc/terms/family)
* subfamily: "dwc:subfamily" ([http://rs.tdwg.org/dwc/terms/subfamily](http://rs.tdwg.org/dwc/terms/subfamily))
* genus: "dwc:genus" ([http://rs.tdwg.org/dwc/terms/genus](http://rs.tdwg.org/dwc/terms/genus))
* subgenus: "dwc:subgenus" ([http://rs.tdwg.org/dwc/terms/subgenus](http://rs.tdwg.org/dwc/terms/subgenus))
* specificEpithet: "dwc:specificEpithet" ([http://rs.tdwg.org/dwc/terms/specificEpithet](http://rs.tdwg.org/dwc/terms/specificEpithet))
* infraspecificEpithet: "dwc:infraspecificEpithet" ([http://rs.tdwg.org/dwc/terms/infraspecificEpithet](http://rs.tdwg.org/dwc/terms/infraspecificEpithet))
* scientificName: "dwc:scientificName" ([http://rs.tdwg.org/dwc/terms/scientificName](http://rs.tdwg.org/dwc/terms/scientificName))
* scientificNameAuthorship: "dwc:scientificNameAuthorship" ([http://rs.tdwg.org/dwc/terms/scientificNameAuthorship](http://rs.tdwg.org/dwc/terms/scientificNameAuthorship))
* acceptedNameUsage: "dwc:acceptedNameUsage" ([http://rs.tdwg.org/dwc/terms/acceptedNameUsage](http://rs.tdwg.org/dwc/terms/acceptedNameUsage))
* namePublishedInYear: "dwc:namePublishedInYear" ([http://rs.tdwg.org/dwc/terms/namePublishedInYear](http://rs.tdwg.org/dwc/terms/namePublishedInYear))
* country: "dwc:country"  ([http://rs.tdwg.org/dwc/terms/country](http://rs.tdwg.org/dwc/terms/country))
* Locality: "dwc:locality" ([http://rs.tdwg.org/dwc/terms/locality](http://rs.tdwg.org/dwc/terms/locality))
* locationRemarks: "dwc:locationRemarks" ([http://rs.tdwg.org/dwc/terms/locationRemarks](http://rs.tdwg.org/dwc/terms/locationRemarks))
* habitat: "dwc:habitat" ([http://rs.tdwg.org/dwc/terms/habitat](http://rs.tdwg.org/dwc/terms/habitat))
* decimalLongitude: "dwc:decimalLongitude" ([http://rs.tdwg.org/dwc/terms/decimalLongitude](http://rs.tdwg.org/dwc/terms/decimalLongitude))
* decimalLatitude: "dwc:decimalLatitude" ([http://rs.tdwg.org/dwc/terms/decimalLatitude](http://rs.tdwg.org/dwc/terms/decimalLatitude))
* geodeticDatum: "dwc:geodeticDatum" ([http://rs.tdwg.org/dwc/terms/geodeticDatum](http://rs.tdwg.org/dwc/terms/geodeticDatum))
* Easting_EPSG3035: easting coordinates in ETRS89-extended / LAEA Europe (EPSG: 3035) projected coordinate system.
* Northing_EPSG3035: northing coordinates in ETRS89-extended / LAEA Europe (EPSG: 3035) projected coordinate system.
* Coord.Uncertainty: spatial uncertainty in the provided coordinates (spanning from 0.1 km to "Region").
* Coord.Validator: person who performed the assessment of the spatial uncertainty of records' coordinates.
* associatedReferences: "dwc:associatedReferences" ([http://rs.tdwg.org/dwc/terms/associatedReferences](http://rs.tdwg.org/dwc/terms/associatedReferences))
* source: literature, personal collection or research project from which the single records were obatained.
* researchGroup: researchers involved in the project during which the single records were collected.

## Code/software

Data can be viewed and processed in several open software (e.g. R, QGIS, Python).
