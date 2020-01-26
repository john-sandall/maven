# General Election datasets

If you have any questions about these datasets please [contact me @John_Sandall](https://twitter.com/John_Sandall) on Twitter.


## Sources
We aim to source our data directly from the most authorative data provider, falling back to less authorative sources where a primary source isn't available. By country:

- **United Kingdom:** [Electoral Commission](http://www.electoralcommission.org.uk/our-work/our-research/electoral-data).


## Data dictionaries

#### **`general-election/UK/2015/model`**
| Column | Type | Description | Example |
| -- | -- | -- | -- |
| `Press Association Reference` | int | Standardised constituency identifier | `1` |
| `Constituency Name` | str | Constituency name | `Aberavon` |
| `Region` | str | Region:{`East Midlands`, `Eastern`, `London`, `North East`, `North West`, `Northern Ireland`, `Scotland`, `South East`, `South West`, `Wales`, `West Midlands`, `Yorkshire and The Humber`} | `Wales` |
| `Electorate` | int | Electorate | `50838` |
| `Votes` | int | Valid votes counted | `30958` |
| `Party` | str | Party | `con` |
| `votes_last` | int | Votes counted in 2010 | `4411` |
| `pc_last` | float | Percentage voteshare in 2010 | `0.142483365` |
| `win_last` | str | Which party won in this constituency in 2010 | `lab` |
| `polls_now` | float | National polling for this party in 2015 | `0.338181818` |
| `swing_now` | float | Uplift in national polling for this party since 2010 | `-0.062020512` |
| `swing_forecast_pc` | float | Projected voteshare for this party in this constituency using a UNS model | `0.133646473` |
| `swing_forecast_win` | str | Projected winner in this constituency using a UNS model | `lab` |
| `actual_win_now` | str | Which party actually won this constituency in 2015? | `lab` |
| `actual_pc_now` | float | Actual percentage voteshare for this party in this constituency in 2015 | `0.118706976` |
| `con` | int | Dummy: is Conservative party? | `1` |
| `grn` | int | Dummy: is Green party? | `0` |
| `lab` | int | Dummy: is Labour party? | `0` |
| `ld` | int | Dummy: is Liberal Democrat party? | `0` |
| `Region_East Midlands` | int | Dummied region | `0` |
| `Region_Eastern` | int | Dummied region | `0` |
| `Region_London` | int | Dummied region | `0` |
| `Region_North East` | int | Dummied region | `0` |
| `Region_North West` | int | Dummied region | `0` |
| `Region_Northern Ireland` | int | Dummied region | `0` |
| `Region_Scotland` | int | Dummied region | `0` |
| `Region_South East` | int | Dummied region | `0` |
| `Region_South West` | int | Dummied region | `0` |
| `Region_Wales` | int | Dummied region | `1` |
| `Region_West Midlands` | int | Dummied region | `0` |
| `Region_Yorkshire and the Humber` | int | Dummied region | `0` |
| `won_here_last` | int | Did this party win this constituency in 2010? | `0` |
| `turnout` | float | Turnout in 2015 | `0.608953932` |


#### **`general-election/UK/2010/results`**
| Column            | Type  | Description | Example |
| --                | -- | -- | -- |
| `ons_id`          | str   | Standardised constituency identifier | `E14000530` |
| `constituency`    | str   | Constituency name | `ALDERSHOT` |
| `county`          | str   | County name | `Hampshire` |
| `region`          | str   | Region:{`East Midlands`, `Eastern`, `London`, `North East`, `North West`, `Northern Ireland`, `Scotland`, `South East`, `South West`, `Wales`, `West Midlands`, `Yorkshire and The Humber`} | `South East` |
| `country`         | str   | Country:{`England`, `Northern Ireland`, `Scotland`, `Wales`} | `England` |
| `electorate`      | int   | Electorate | `71465` |
| `total_votes`     | int   | Total valid votes counted in this constituency | `45384` |
| `turnout`         | float | Turnout in this constituency | `0.635052123` |
| `party`           | str   | Name of political party (lower-cased & abbreviated) | `con` |
| `votes`           | int   | Votes for this party | `21203` |
| `voteshare`       | float | Vote share for this party within the constituency | `0.467191081` |


#### **`general-election/UK/2015/results`**
| Column            | Type  | Description | Example |
| --                | -- | -- | -- |
| `ons_id`          | str   | Standardised constituency identifier | `E14000530` |
| `constituency`    | str   | Constituency name | `ALDERSHOT` |
| `county`          | str   | County name | `Hampshire` |
| `region`          | str   | Region:{`East Midlands`, `Eastern`, `London`, `North East`, `North West`, `Northern Ireland`, `Scotland`, `South East`, `South West`, `Wales`, `West Midlands`, `Yorkshire and The Humber`} | `South East` |
| `country`         | str   | Country:{`England`, `Northern Ireland`, `Scotland`, `Wales`} | `England` |
| `electorate`      | int   | Electorate | `72430` |
| `total_votes`     | int   | Total valid votes counted in this constituency | `46191` |
| `turnout`         | float | Turnout in this constituency | `0.637732984` |
| `party`           | str   | Name of political party (lower-cased & abbreviated) | `con` |
| `votes`           | int   | Votes for this party | `23369` |
| `voteshare`       | float | Vote share for this party within the constituency | `0.505921067` |


#### **`general-election/UK/2017/results`**
| Column            | Type  | Description | Example |
| --                | -- | -- | -- |
| `ons_id`          | str   | Standardised constituency identifier | `E14000530` |
| `constituency`    | str   | Constituency name | `ALDERSHOT` |
| `county`          | str   | County name | `Hampshire` |
| `region`          | str   | Region:{`East Midlands`, `Eastern`, `London`, `North East`, `North West`, `Northern Ireland`, `Scotland`, `South East`, `South West`, `Wales`, `West Midlands`, `Yorkshire and The Humber`} | `South East` |
| `country`         | str   | Country:{`England`, `Northern Ireland`, `Scotland`, `Wales`} | `England` |
| `electorate`      | int   | Electorate | `76205` |
| `total_votes`     | int   | Total valid votes counted in this constituency | `48950` |
| `turnout`         | float | Turnout in this constituency | `0.642346303` |
| `party`           | str   | Name of political party (lower-cased & abbreviated) | `con` |
| `votes`           | int   | Votes for this party | `26950` |
| `voteshare`       | float | Vote share for this party within the constituency | `0.550561798` |


#### **`general-election/UK/polls`**
| Column | Type | Description | Example |
| -- | -- | -- | -- |
| `company` | str | Name of company conducting opinion poll | `Ipsos MORI Phone` |
| `client` | str | Name of client/publisher commissioning the poll | `Evening Standard` |
| `method` | str | Methodology: {`Online`, `Phone`, `Mobile`} | `Phone` |
| `from` | date | Date fieldwork started | `2017-06-06` |
| `to` | date | Date fieldwork completed | `2017-06-07` |
| `sample_size` | int | Sample size of poll | `1291` |
| `con` | float | National percentage voteshare for the Conservative party | `0.44` |
| `lab` | float | National percentage voteshare for the Labour party | `0.36` |
| `ld` | float | National percentage voteshare for the Liberal Democrat party | `0.07` |
| `ukip` | float | National percentage voteshare for UKIP | `0.04` |
| `grn` | float | National percentage voteshare for the Green party | `0.02` |
| `snp` | float | National percentage voteshare for the SNP | `0.05` |
| `pdf` | str | Download URL of PDF tables containing raw data | `https://www.ipsos.com/sites/default/files/2017-06/pm-election-2017-final-tables.pdf` |
