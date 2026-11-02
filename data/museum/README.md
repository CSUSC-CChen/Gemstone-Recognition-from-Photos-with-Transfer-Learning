# Museum and personal-collection test set

A small real-world test set, to check whether a model trained on web images still works on photos a person takes. It is used only for testing, never for training or tuning.

## Sources

* Stones on public display in the Robert Procop Gem and Mineral Hall, Natural History Museum of Los Angeles County. Photographed by me without flash.
* Stones from my personal collection.

Ground-truth labels come from the museum's display cards. For personal stones, the label is what the stone was sold as.

## Photo rules

* One stone per photo, filling about half the frame, shot roughly from above.
* For museum stones, also photograph the display card, then crop the card out of the test photo.
* Resize photos so the longer side is about 1024 pixels before committing.
* Crop out other visitors and anything personal.

## File names

`<class>_<source><number>_<type>_a<angle>.jpg`

* `source`: `museum` or `own`
* `type`: `faceted`, `cabochon`, or `rough`
* Example: `peridot_museum01_faceted_a01.jpg`, `lapis_own01_cabochon_a02.jpg`

All photos of one physical stone share the same `<class>_<source><number>` part. Results are reported per stone, so extra angles of one stone never count as separate stones.

## labels.csv

One row per photo:

| Column | Meaning |
|---|---|
| `file` | file name in `photos/` |
| `object_id` | one ID per physical stone, for example `peridot_museum01` |
| `display_label` | the label on the museum card, exactly as written |
| `kaggle_class` | matching Kaggle class name, or blank if there is no match |
| `type` | `faceted`, `cabochon`, or `rough` |
| `source` | `museum` or `own` |
| `notes` | anything unusual: lab-grown, star or cat's-eye effect, glare |

## Mapping museum labels to Kaggle classes

Kaggle splits some minerals by color and garnets by species. Use the class names exactly as they appear in `data/splits/train.csv`.

| Display label | Kaggle class |
|---|---|
| Blue / pink / purple / golden (yellow) sapphire | Sapphire Blue / Sapphire Pink / Sapphire Purple / Sapphire Yellow |
| Ruby | Ruby |
| Spinel (any color) | Spinel |
| Opal (black, jelly, white) | Opal |
| Diamond (any color) | Diamond |
| Peridot | Peridot |
| Lapis lazuli | Lapis Lazuli |
| Almandine, pyrope, spessartite, grossular, andradite garnet | the matching species class |
| "Garnet" with no species | leave `kaggle_class` blank |
| Green, orange, colorless, sherry, wine, bi-color sapphire | no class, leave blank |

Rows with a blank `kaggle_class` are kept for reference but left out of accuracy.
