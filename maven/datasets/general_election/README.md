# General Election datasets

If you have any questions about these datasets please [contact me @John_Sandall](https://twitter.com/John_Sandall) on Twitter.


## Sources
We aim to source our data directly from the most authorative data provider, falling back to less authorative sources where a primary source isn't available. By country:

- **United Kingdom:** [Electoral Commission](http://www.electoralcommission.org.uk/our-work/our-research/electoral-data).


## Data dictionaries

#### **`general_election-gb-2015-results`**
| Column | Type | Description | Example |
| -- | -- | -- | -- |
| `Press Association ID Number` | int | Standardised constituency identifier | `1` |
| `Constituency ID` | str | ONS constituency identifier | `W07000049` |
| `Constituency Name` | str | Name | `Aberavon` |
| `Constituency Type` | str | Type | One of `Borough`, `Burgh`, `County` |
| `County` | str | Country | `West Glamorgan` |
| `Region ID` | str | ONS region identifier | `W92000004` |
| `Region` | str | Region | One of `East`, `East Midlands`, `London`, `North East`, `North West`, `Northern Ireland`, `Scotland`, `South East`, `South West`, `Wales`, `West Midlands`, `Yorkshire and The Humber` |
| `Country` | str | Country | One of `England`, `Northern Ireland`, `Scotland`, `Wales` |
| `Election Year` | int | Year | Always `2015` |
| `Electorate` | int | Electorate | `49821` |
| `Valid Votes` | int | Valid votes counted | `31523` |
| The remaining columns are all parties | | | |
| -- | -- | -- | -- |
| `30-50` | int | Votes for "30-50" party in this constituency | `0` |
| `Above` | int | Votes for "Above" party in this constituency  | `0` |
| ... | ... | ... | ... |
| `C` | int | Votes for the Conservative party in this constituency  | `3742` |
| ... | ... | ... | ... |
| `Lab` | int | Votes for the Labour party in this constituency  | `15416` |
| `Lab Co-op` | int | Votes for the Labour Co-op party in this constituency  | `0` |
| ... | ... | ... | ... |
| `Zeb` | int | Votes for the "Zeb" party in this constituency  | `0` |
