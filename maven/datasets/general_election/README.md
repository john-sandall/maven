# General Election datasets

If you have any questions about these datasets please [contact me @John_Sandall](https://twitter.com/John_Sandall) on Twitter.


## Sources
We aim to source our data directly from the most authorative data provider, falling back to less authorative sources where a primary source isn't available. By country:
- **United Kingdom:** [House of Commons Library](https://researchbriefings.parliament.uk/ResearchBriefing/Summary/CBP-8647).


## Data dictionaries

#### **`general-election/UK/2015/model`**
| Column | Type | Description | Example |
| -- | -- | -- | -- |
| Constituency-level factors |
| `ons_id` | int | ONS constituency identifier | `E14000530` |
| `constituency` | str | Constituency name | `ALDERSHOT` |
| `county` | str | County:{`Avon`, `Bedfordshire`, and 44 more} | `Hampshire` |
| `region` | str | Region:{`East Midlands`, `Eastern`, `London`, `North East`, `North West`, `Northern Ireland`, `Scotland`, `South East`, `South West`, `Wales`, `West Midlands`, `Yorkshire and The Humber`} | `South East` |
| `geo` | str | Geographic region (aggregated level between region and country) | `england_not_london` |
| `country`| str | Country:{`England`, `Northern Ireland`, `Scotland`, `Wales`} | `England` |
| 2010 election data |
| `electorate` | int | Electorate | `72430` |
| `total_votes_last` | int | Total valid votes counted in this constituency in the 2010 election | `45384` |
| `turnout_last` | float | Turnout in this constituency in the 2010 election | `0.635052123` |
| `party` | str | Party:{`apni`, `con`, `dup`, `grn`, `lab`, `ld`, `other`, `pc`, `sdlp`, `sf`, `snp`, `ukip`, `uup`} | `con` |
| `votes_last` | int | Votes counted for this party in this constituency in 2010 | `21203` |
| `voteshare_last` | float | Percentage voteshare for this party in this constituency in 2010 | `0.467191` |
| `winner_last` | str | Party that won in this constituency in 2010 | `con` |
| `won_here_last` | bool | Did this party win in this constituency in 2010 | `True` |
| `national_voteshare_last` | float | Percentage of national voteshare for this party from 2010 results | `0.360542872` |
| 2015 pre-election data |
| `national_polls_now` | float | Percentage of national voteshare for this party from 2015 pre-election polling | `0.338181818` |
| `national_swing` | float | Uplift in national voteshare for this party between 2010 results and 2015 polling | `-0.062020512` |
| `national_swing_forecast` | str | Projected voteshare for this party in this constituency using a UNS model | `0.438215651` |
| `national_swing_winner` | str | Projected winner in this constituency using `national_swing_forecast` | `con` |
| 2015 post-election data |
| `total_votes_now` | int | Total valid votes counted in this constituency in the 2015 election | `46191` |
| `turnout_now` | float | Turnout in this constituency in 2015 election | `0.637732984` |
| `votes_now` | int | Total votes counted for this party in this constituency in 2015 | `23369` |
| `voteshare_now` | float | Percentage voteshare for this party in this constituency in 2015 | `0.505921067` |
| `winner_now` | str | Party that won in this constituency in 2015 | `con` |


#### **`general-election/UK/2017/model`**
| Column | Type | Description | Example |
| -- | -- | -- | -- |
| Constituency-level factors |
| `ons_id` | int | ONS constituency identifier | `E14000530` |
| `constituency` | str | Constituency name | `ALDERSHOT` |
| `county` | str | County:{`Avon`, `Bedfordshire`, and 44 more} | `Hampshire` |
| `region` | str | Region:{`East Midlands`, `Eastern`, `London`, `North East`, `North West`, `Northern Ireland`, `Scotland`, `South East`, `South West`, `Wales`, `West Midlands`, `Yorkshire and The Humber`} | `South East` |
| `geo` | str | Geographic region (aggregated level between region and country) | `england_not_london` |
| `country`| str | Country:{`England`, `Northern Ireland`, `Scotland`, `Wales`} | `England` |
| 2015 election data |
| `electorate` | int | Electorate | `76205` |
| `total_votes_last` | int | Total valid votes counted in this constituency in the 2015 election | `46191` |
| `turnout_last` | float | Turnout in this constituency in the 2015 election | `0.637732984` |
| `party` | str | Party:{`apni`, `con`, `dup`, `grn`, `lab`, `ld`, `other`, `pc`, `sdlp`, `sf`, `snp`, `ukip`, `uup`} | `con` |
| `votes_last` | int | Votes counted for this party in this constituency in 2015 | `23369` |
| `voteshare_last` | float | Percentage voteshare for this party in this constituency in 2015 | `0.505921067` |
| `winner_last` | str | Party that won in this constituency in 2015 | `con` |
| `won_here_last` | bool | Did this party win in this constituency in 2015 | `True` |
| `national_voteshare_last` | float | Percentage of national voteshare for this party from 2015 results | `0.368095115` |
| 2017 pre-election data |
| `national_polls_now` | float | Percentage of national voteshare for this party from 2017 pre-election polling | `0.42729587` |
| `national_swing` | float | Uplift in national voteshare for this party between 2015 results and 2017 polling | `0.160830048` |
| `national_swing_forecast` | str | Projected voteshare for this party in this constituency using a UNS model | `0.587288376` |
| `national_swing_winner` | str | Projected winner in this constituency using `national_swing_forecast` | `con` |
| 2015/2017 regional data |
| `geo_polls_now` | float | Percentage of regional voteshare for this party from 2017 pre-election polling | `0.470077263` |
| `geo_voteshare_last` | float | Percentage of regional voteshare for this party from 2015 results | `0.418216805` |
| `geo_swing` | float | Uplift in regional voteshare for this party between 2015 results and 2017 polling | `0.124003764` |
| `geo_swing_forecast` | float | Projected voteshare for this party in this constituency using a regional UNS model | `0.568657183` |
| `geo_swing_winner` | str | Projected winner in this constituency using `geo_swing_forecast` | `con` |
| 2017 post-election data |
| `total_votes_now` | int | Total valid votes counted in this constituency in the 2017 election | `48950` |
| `turnout_now` | float | Turnout in this constituency in 2017 election | `0.642346303` |
| `votes_now` | int | Total votes counted for this party in this constituency in 2017 | `26950` |
| `voteshare_now` | float | Percentage voteshare for this party in this constituency in 2017 | `0.550561798` |
| `winner_now` | str | Party that won in this constituency in 2017 | `con` |


#### **`general-election/UK/2019/model`**
| Column | Type | Description | Example |
| -- | -- | -- | -- |
| Constituency-level factors |
| `ons_id` | int | ONS constituency identifier | `E14000530` |
| `constituency` | str | Constituency name | `ALDERSHOT` |
| `county` | str | County:{`Avon`, `Bedfordshire`, and 44 more} | `Hampshire` |
| `region` | str | Region:{`East Midlands`, `Eastern`, `London`, `North East`, `North West`, `Northern Ireland`, `Scotland`, `South East`, `South West`, `Wales`, `West Midlands`, `Yorkshire and The Humber`} | `South East` |
| `geo` | str | Geographic region (aggregated level between region and country) | `england_not_london` |
| `country`| str | Country:{`England`, `Northern Ireland`, `Scotland`, `Wales`} | `England` |
| 2017 election data |
| `electorate` | int | Electorate | `76205` |
| `total_votes_last` | int | Total valid votes counted in this constituency in the 2017 election | `48950` |
| `turnout_last` | float | Turnout in this constituency in the 2017 election | `0.642346303` |
| `party` | str | Party:{`apni`, `con`, `dup`, `grn`, `lab`, `ld`, `other`, `pc`, `sdlp`, `sf`, `snp`, `ukip`, `uup`} | `con` |
| `votes_last` | int | Votes counted for this party in this constituency in 2017 | `26950` |
| `voteshare_last` | float | Percentage voteshare for this party in this constituency in 2017 | `0.550561798` |
| `winner_last` | str | Party that won in this constituency in 2017 | `con` |
| `won_here_last` | bool | Did this party win in this constituency in 2017 | `True` |
| `national_voteshare_last` | float | Percentage of national voteshare for this party from 2017 results | `0.423444482` |
| 2019 pre-election data |
| `national_polls_now` | float | Percentage of national voteshare for this party from 2019 pre-election polling | `0.396538462` |
| `national_swing` | float | Uplift in national voteshare for this party between 2017 results and 2019 polling | `-0.063540845` |
| `national_swing_forecast` | str | Projected voteshare for this party in this constituency using a UNS model | `0.515578636` |
| `national_swing_winner` | str | Projected winner in this constituency using `national_swing_forecast` | `con` |
| 2017/2019 regional data |
| `geo_polls_now` | float | Percentage of regional voteshare for this party from 2019 pre-election polling | `0.429089129` |
| `geo_voteshare_last` | float | Percentage of regional voteshare for this party from 2017 results | `0.474642379` |
| `geo_swing` | float | Uplift in regional voteshare for this party between 2017 results and 2019 polling | `-0.095973837` |
| `geo_swing_forecast` | float | Projected voteshare for this party in this constituency using a regional UNS model | `0.497722269` |
| `geo_swing_winner` | str | Projected winner in this constituency using `geo_swing_forecast` | `con` |


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
