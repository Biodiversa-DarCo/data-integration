# Examples

<script setup>
import { withBase } from 'vitepress'
</script>

The <a :href="withBase('/template.xlsx')" target="_blank" ref="external">dataset template file</a> includes a sheet with several example records.
This page contains some explanations about these examples.

- **Line 2:** \
  One occurrence of *Asellus aquaticus cavernicolus* at site `PIVKACAV`.
- **Lines 3-5:** \
  One occurrence of *Asellus kosswigi* at site `MERAVIGL`, for which we register 3 sequences.
  Only the first line defines all the infos related to the site, sampling and identification of the occurrence.
  It also includes an `occurrence_id`, which can be any arbitrary string.
  Lines 3 and 4 repeat the `occurrence_id`, to indicate that this is the same occurrence and that they only describe a sequence attached to the occurrence.
- **Line 6-7:** \
  Two distinct occurrences, that were sampled on the same site `TREBICGR`.
  Both of them identify the same taxon *Asellus kosswigi*, but were sampled at different times (one of them at an unknown date).
  Site informations for `TREBICGR` are only defined for one of them,
  the other just needs to repeat the `site_code`.
- **Line 8:** \
  One occurrence with uncertain assignation (*Proasellus cf. lescherae*). Uncertainty status is indicated by column `tax_id_confer` = `true`.
- **Line 9:** \
  One occurrence with assignation to an unclassified taxon, with affinity to an existing species (*Proasellus aff. escolai*).
  Under the hood, a new taxon named `Proasellus aff. escolai` with rank species and status "Unclassified" will be registered in the taxonomy under the genus Proasellus.
- **Line 10:** \
  An example of occurrence with assignation to a subgenus taxon *Graeteriella (Paragraeteriella)*.
- **Line 11-12:**
  - Line 11: One occurrence with assignation to a new unclassified taxon *Proasellus anophtalmus aff. rhausinus form A* with an addendum (form A).
  Since this is an unclassified taxon, the addendum can be included in the `taxon_name`.
  - Line 12: One occurrence with assignation to an unspecified species in the genus Diacyclops, refined to "group languidoides" specified as `tax_id_addendum`.
  As opposed to the previous occurrence record, this occurrence is assigned to an already referenced taxon (Diacyclops),
  but adds precision about the identification without creating or modifying any taxon.
  The resulting identification will read as `Diacyclops sp. group languidoides` and point to taxon Diacyclops under the hood.