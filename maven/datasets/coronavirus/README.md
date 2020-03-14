# Coronavirus (COVID-19) datasets

If you have any questions about these datasets please [contact me @John_Sandall](https://twitter.com/John_Sandall) on Twitter.


## Sources
We aim to source our data directly from the most authorative data provider, falling back to less authorative sources where a primary source isn't available.

Global providers/aggregators:
- [Johns Hopkins Center for Systems Science and Engineering](https://github.com/CSSEGISandData).


## Data dictionaries

#### **`coronavirus/CSSE`**

##### `CSSE_country_province.csv`
| Column | Type | Description | Example |
| -- | -- | -- | -- |
| `date` | date | Date | `2020-03-13` |
| `country_region` | str | Country/Region | `US` |
| `province_state` | str | Province/State | `Washington` |
| `lat` | float | Latitude | `47.4009` |
| `lon` | float | Longitude | `-121.4905` |
| `confirmed` | int | Confirmed cases | `568` |
| `deaths` | int | Fatalities | `37` |
| `recovered` | int | Recovered | `1` |

##### `CSSE_country.csv`
| Column | Type | Description | Example |
| -- | -- | -- | -- |
| `date` | date | Date | `2020-03-13` |
| `country_region` | str | Country/Region | `US` |
| `confirmed` | int | Confirmed cases | `2179` |
| `deaths` | int | Fatalities | `47` |
| `recovered` | int | Recovered | `12` |
