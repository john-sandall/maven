# General Election datasets

If you have any questions about these datasets please [contact me @John_Sandall](https://twitter.com/John_Sandall) on Twitter.


## Sources
We aim to source our data directly from the most authorative data provider, falling back to less authorative sources where a primary source isn't available. By country:

- **United Kingdom:** [Electoral Commission](http://www.electoralcommission.org.uk/our-work/our-research/electoral-data).


## Data dictionaries

#### **`general-election/GB/2015/results`**
| Column | Type | Description | Example |
| -- | -- | -- | -- |
| `Press Association ID Number` | int | Standardised constituency identifier | `1` |
| `Constituency ID` | str | ONS constituency identifier | `W07000049` |
| `Constituency Name` | str | Name | `Aberavon` |
| `Constituency Type` | str | Type: {`Borough`, `Burgh`, `County`} | `County` |
| `County` | str | Country | `West Glamorgan` |
| `Region ID` | str | ONS region identifier | `W92000004` |
| `Region` | str | Region:{`East`, `East Midlands`, `London`, `North East`, `North West`, `Northern Ireland`, `Scotland`, `South East`, `South West`, `Wales`, `West Midlands`, `Yorkshire and The Humber`} | `Wales` |
| `Country` | str | Country: {`England`, `Northern Ireland`, `Scotland`, `Wales`} | `Wales` |
| `Election Year` | int | Year | Always `2015` |
| `Electorate` | int | Electorate | `49821` |
| `Valid Votes` | int | Valid votes counted | `31523` |
| `con` | int | Votes for the Conservative party in this constituency | `3742` |
| `lab` | int | Votes for the Labour party in this constituency | `15416` |
| `ld` | int | Votes for the Liberal Democrat party in this constituency | `1397` |
| `ukip` | int | Votes for the UKIP party in this constituency | `4971` |
| `grn` | int | Votes for the Green party in this constituency | `711` |
| `snp` | int | Votes for SNP in this constituency | `0` |
| `pc` | int | Votes for Plaid Cymru in this constituency | `3663` |
| `other` | int | Votes for all other parties (combined) in this constituency | `1623` |
| `con_pc` | float | Percentage voteshare for the Conservative party in this constituency | `0.118707` |
| `lab_pc` | float | Percentage voteshare for the Labour party in this constituency | `0.48904` |
| `ld_pc` | float | Percentage voteshare for the Liberal Democrat party in this constituency | `0.0443168` |
| `ukip_pc` | float | Percentage voteshare for the UKIP party in this constituency | `0.157694` |
| `grn_pc` | float | Percentage voteshare for the Green party in this constituency | `0.022555` |
| `snp_pc` | float | Percentage voteshare for SNP in this constituency | `0` |
| `pc_pc` | float | Percentage voteshare for Plaid Cymru in this constituency | `0.116201` |
| `other_pc` | float | Percentage voteshare for all other parties (combined) in this constituency | `0.0514862` |
| `winner` | str | Winning party with most votes in this constituency  | `lab` |
| `geo` | str | Model-specific regions: {`Wales`, `Scotland`, `England_not_london`, `NI`, `London`}  | `Wales` |
