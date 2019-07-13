"""
Model-ready dataset for the United Kingdom's 2015 General Election.

Usage:
    > import maven
    > maven.get('general-election/UK/2015/model', data_directory='./data/')
"""
import os
from pathlib import Path
import shutil

import pandas as pd

import maven


class UK2015Model:
    """Generates model-ready data for the United Kingdom's 2015 General Election."""

    def __init__(self, directory=Path('data/general-election/UK/2015/model')):
        self.directory = Path(directory)

    def retrieve(self):
        """Will check to see if this already exists in directory tree, otherwise puts the
           datasets there by executing the necessary code from within this repo."""
        destination_target = self.directory / 'raw'
        os.makedirs(destination_target, exist_ok=True)  # create directory if it doesn't exist
        data_directory = (self.directory / '..' / '..' / '..' / '..').resolve()  # sensible guess
        data = [
            # (identifier, type, filename)
            ('general-election/UK/2010/results', 'processed', 'general_election-uk-2010-results.csv'),
            ('general-election/UK/2010/results', 'processed', 'general_election-uk-2010-results-full.csv'),
            ('general-election/UK/2015/results', 'processed', 'general_election-uk-2015-results.csv'),
            ('general-election/UK/2015/results', 'processed', 'general_election-uk-2015-results-full.csv'),
            ('general-election/UK/polls', 'processed', 'general_election-uk-polls.csv'),
            ('general-election/UK/polls', 'processed', 'general_election-london-polls.csv'),
            ('general-election/UK/polls', 'processed', 'general_election-scotland-polls.csv'),
            ('general-election/UK/polls', 'processed', 'general_election-wales-polls.csv'),
            ('general-election/UK/polls', 'processed', 'general_election-ni-polls.csv'),
        ]
        for identifier, data_type, filename in data:
            source_target = f"{identifier}/{data_type}/{filename}"
            if not (data_directory / source_target).is_file():
                print(f'Dataset {identifier} not found - retrieving now')
                maven.get(identifier, data_directory=data_directory)
            shutil.copyfile(
                src=data_directory / source_target,
                dst=destination_target / filename
            )

    def process(self):
        """Process results data from the United Kingdom's 2010 and 2015 General Elections
           into a single model-ready dataset for predicting the 2015 General Election."""
        processed_directory = (self.directory / 'processed')
        os.makedirs(processed_directory, exist_ok=True)  # create directory if it doesn't exist

        # TODO: Refactor these sections into functions to make it easier to read.

        #############
        # IMPORT DATA
        #############

        # Import general election results
        ge_2010 = pd.read_csv(self.directory / 'raw' / 'general_election-uk-2010-results.csv')
        ge_2010_full = pd.read_csv(self.directory / 'raw' / 'general_election-uk-2010-results-full.csv')
        ge_2015 = pd.read_csv(self.directory / 'raw' / 'general_election-uk-2015-results.csv')
        ge_2015_full = pd.read_csv(self.directory / 'raw' / 'general_election-uk-2015-results-full.csv')
        polls = pd.read_csv(self.directory / 'raw' / 'general_election-uk-polls.csv')

        # Check constituencies are mergeable
        assert set(ge_2010['Press Association Reference']).difference(set(ge_2015['Press Association ID Number'])) == set()
        assert set(ge_2015['Press Association ID Number']).difference(set(ge_2010['Press Association Reference'])) == set()
        assert len(ge_2010) == len(ge_2010['Press Association Reference']) == 650
        assert len(ge_2015) == len(ge_2015['Press Association ID Number']) == 650

        # Construct some lookups of the parties we want to model
        parties_lookup_2010 = {
            'Con': 'con',
            'Lab': 'lab',
            'LD': 'ld',
            'UKIP': 'ukip',
            'Grn': 'grn',
            'Other': 'other'
        }
        parties_15 = list(parties_lookup_2010.values())

        parties_lookup_2015 = {
            'C': 'con',
            'Lab': 'lab',
            'LD': 'ld',
            'UKIP': 'ukip',
            'Green': 'grn',
            'SNP': 'snp',
            'PC': 'pc',
            'Other': 'other'
        }
        parties_17 = list(parties_lookup_2015.values())

        ##############
        # 2015 POLLING
        ##############

        # Get 2015 polling
        pollsters = polls[(polls.to >= '2015-04-04') & (polls.to <= '2015-05-04')].company.unique()

        # Use single last poll from each pollster in final week of polling then average out
        polls = polls[(polls.to >= '2015-04-01') & (polls.to <= '2015-05-07')]
        pop = polls.loc[:0]
        for p in pollsters:
            pop = pop.append(polls[polls.company == p].tail(1))

        # Create new polls dictionary by geo containing simple average across all pollsters
        polls = {'UK': {}}
        for p in ['con', 'lab', 'ld', 'ukip', 'grn']:
            polls['UK'][p] = pop[p].mean()
        polls['UK'] = pd.Series(polls['UK'])

        # Scotland, Wales, NI, London not available in 2015 data (we haven't extracted them yet!)
        # Add Other
        for geo in ['UK']:
            if 'other' not in polls[geo]:
                polls[geo]['other'] = 1 - sum(polls[geo])

        # Reweight to 100%
        for geo in ['UK']:
            polls[geo] = polls[geo] / polls[geo].sum()

        ##############
        # 2017 POLLING
        ##############
        # TODO: This is messy.
        # TODO: This should be in the polling processing pipeline.
        # Latest polling data
        polls_17 = {'UK': {}}
        polls_17_uk = pd.read_csv(self.directory / 'raw' / 'general_election-uk-polls.csv')
        # Filter to recent data
        polls_17_uk = polls_17_uk[polls_17_uk.to >= '2017-06-06']
        # Add parties
        for p in ['con', 'lab', 'ld', 'ukip', 'grn', 'snp']:
            polls_17['UK'][p] = (polls_17_uk.sample_size * polls_17_uk[p]).sum() / polls_17_uk.sample_size.sum()
        polls_17['UK'] = pd.Series(polls_17['UK'], index=['con', 'lab', 'ld', 'ukip', 'snp', 'grn'])

        # Repeat for Scotland polling...
        polls_17['Scotland'] = {}
        polls_17_tmp = pd.read_csv(self.directory / 'raw' / 'general_election-scotland-polls.csv')
        polls_17_tmp = polls_17_tmp[polls_17_tmp.to >= '2017-06-05']
        for p in ['con', 'lab', 'ld', 'ukip', 'snp', 'grn']:
            polls_17['Scotland'][p] = (polls_17_tmp.sample_size * polls_17_tmp[p]).sum() / polls_17_tmp.sample_size.sum()
        polls_17['Scotland'] = pd.Series(polls_17['Scotland'], index=['con', 'lab', 'ld', 'ukip', 'snp', 'grn'])

        # ...and Wales
        polls_17['Wales'] = {}
        polls_17_tmp = pd.read_csv(self.directory / 'raw' / 'general_election-wales-polls.csv')
        polls_17_tmp = polls_17_tmp[polls_17_tmp.to >= '2017-06-07']
        for p in ['con', 'lab', 'ld', 'ukip', 'pc', 'grn']:
            polls_17['Wales'][p] = (polls_17_tmp.sample_size * polls_17_tmp[p]).sum() / polls_17_tmp.sample_size.sum()
        polls_17['Wales'] = pd.Series(polls_17['Wales'], index=['con', 'lab', 'ld', 'ukip', 'pc', 'grn'])

        # NI
        polls_17['NI'] = (pd.read_csv(self.directory / 'raw' / 'general_election-ni-polls.csv')
                            .sort_values(by='to', ascending=False).iloc[0])
        # Collate all NI parties under other
        for k in polls_17['NI'].index:
            if k not in parties_17:
                del polls_17['NI'][k]

        del polls_17['NI']['other']

        # London
        polls_17['London'] = {}
        polls_17_tmp = pd.read_csv(self.directory / 'raw' / 'general_election-london-polls.csv')
        polls_17_tmp = polls_17_tmp[polls_17_tmp.to >= '2017-05-31']
        for p in ['con', 'lab', 'ld', 'ukip', 'grn']:
            polls_17['London'][p] = (polls_17_tmp.sample_size * polls_17_tmp[p]).sum() / polls_17_tmp.sample_size.sum()
        polls_17['London'] = pd.Series(polls_17['London'], index=['con', 'lab', 'ld', 'ukip', 'grn'])

        # Estimate polling for England excluding London
        survation_wts = {
            # from http://survation.com/wp-content/uploads/2017/06/Final-MoS-Post-BBC-Event-Poll-020617SWCH-1c0d4h9.pdf
            'Scotland': 85,
            'England': 881,
            'Wales': 67,
            'London': 137,
            'NI': 16
        }
        survation_wts['England_not_london'] = survation_wts['England'] - survation_wts['London']
        survation_wts['UK'] = survation_wts['Scotland'] + survation_wts['England'] + survation_wts['Wales'] + survation_wts['NI']

        def calculate_england_not_london(party):
            out = polls_17['UK'][party] * survation_wts['UK']
            for geo in ['Scotland', 'Wales', 'NI', 'London']:
                if party in polls_17[geo]:
                    out = out - polls_17[geo][party] * survation_wts[geo]
            out = out / survation_wts['England_not_london']
            return out

        polls_17['England_not_london'] = {'pc': 0, 'snp': 0}
        for party in ['con', 'lab', 'ld', 'ukip', 'grn']:
            polls_17['England_not_london'][party] = calculate_england_not_london(party)

        polls_17['England_not_london'] = pd.Series(polls_17['England_not_london'])

        # Fill in the gaps
        for geo in ['UK', 'Scotland', 'Wales', 'NI', 'London', 'England_not_london']:
            for party in ['con', 'lab', 'ld', 'ukip', 'grn', 'snp', 'pc']:
                if party not in polls_17[geo]:
                    #print("Adding {} to {}".format(party, geo))
                    polls_17[geo][party] = 0

        # Fix PC (Plaid Cymru) for UK
        polls_17['UK']['pc'] = polls_17['Wales']['pc'] * survation_wts['Wales'] / survation_wts['UK']

        # Add Other
        for geo in ['UK', 'Scotland', 'Wales', 'NI', 'London', 'England_not_london']:
            if 'other' not in polls_17[geo]:
                polls_17[geo]['other'] = 1 - sum(polls_17[geo])

        # This doesn't work for UK or England_not_london; set current other polling to match 2015 result
        polls_17['UK']['other'] = 0.03 # ge.other.sum() / ge['Valid Votes'].sum()
        polls_17['England_not_london']['other'] = 0.01 # ge[ge.geo == 'England_not_london'].other.sum() / ge[ge.geo == 'England_not_london']['Valid Votes'].sum()

        # Reweight to 100%
        for geo in ['UK', 'Scotland', 'Wales', 'NI', 'London', 'England_not_london']:
            polls_17[geo] = polls_17[geo] / polls_17[geo].sum()

        # Export polling data
        polls_15_csv = pd.DataFrame(columns=['con', 'lab', 'ld', 'ukip', 'grn', 'snp', 'pc', 'other'])
        for geo in polls:
            for party in polls[geo].index:
                polls_15_csv.loc[geo, party] = polls[geo].loc[party]
        #polls_15_csv.to_csv(polls_data_dir / 'final_polls_2015.csv', index=True)

        polls_17_csv = pd.DataFrame(columns=['con', 'lab', 'ld', 'ukip', 'grn', 'snp', 'pc', 'other'])
        for geo in polls_17:
            for party in polls_17[geo].index:
                polls_17_csv.loc[geo, party] = polls_17[geo].loc[party]
        #polls_17_csv.to_csv(polls_data_dir / 'final_polls_2017.csv', index=True)

        #############################
        # Calculate uplifts ("swing")
        #############################

        parties_15 = ['con', 'lab', 'ld', 'ukip', 'grn', 'other']
        parties_17 = ['con', 'lab', 'ld', 'ukip', 'grn', 'snp', 'pc', 'other']

        parties_lookup_2010 = {
            'Con': 'con',
            'Lab': 'lab',
            'LD': 'ld',
            'UKIP': 'ukip',
            'Grn': 'grn',
            'Other': 'other'
        }

        parties_lookup_2015 = {
            'C': 'con',
            'Lab': 'lab',
            'LD': 'ld',
            'UKIP': 'ukip',
            'Green': 'grn',
            'SNP': 'snp',
            'PC': 'pc',
            'Other': 'other'
        }

        # Calculate national voteshare in 2010
        ge_2010_totals = ge_2010.loc[:, ['Votes'] + parties_15].sum()
        ge_2010_voteshare = ge_2010_totals / ge_2010_totals['Votes']
        del ge_2010_voteshare['Votes']
        ge_2010_voteshare

        # Calculate swing between 2015 and latest smoothed polling
        swing = ge_2010_voteshare.copy()
        for party in parties_15:
            swing[party] = polls_15_csv.loc['UK', party] / ge_2010_voteshare[party] - 1
            ge_2010[party + '_swing'] = polls_15_csv.loc['UK', party] / ge_2010_voteshare[party] - 1

        # Forecast is previous result multiplied by swing uplift
        for party in parties_15:
            ge_2010[party + '_forecast'] = ge_2010[party + '_pc'] * (1 + swing[party])

        def pred_15(row):
            return row[[p + '_forecast' for p in parties_15]].sort_values(ascending=False).index[0].replace('_forecast', '')

        #ge_2010['win_10'] = ge_2010_full.apply(win_10, axis=1)
        #ge_2015['win_15'] = ge_2015_full.apply(win_15, axis=1)
        ge_2010['win_15'] = ge_2010.apply(pred_15, axis=1)
        #ge_2010.groupby('win_10').count()['Constituency Name'].sort_values(ascending=False)

        ########################################################
        # Calculate Geo-Level Voteshare + Swing inc. all parties
        ########################################################

        # Add geos
        geos = list(ge_2015.geo.unique())

        # Calculate geo-level voteshare in 2015
        ge_2015_totals = ge_2015.loc[:, ['Valid Votes', 'geo'] + parties_17].groupby('geo').sum()

        # Convert into vote share
        ge_2015_voteshare = ge_2015_totals.div(ge_2015_totals['Valid Votes'], axis=0)
        del ge_2015_voteshare['Valid Votes']
        ge_2015_voteshare

        # Calculate geo-swing
        swing_17 = ge_2015_voteshare.copy()
        for party in parties_17:
            for geo in geos:
                if ge_2015_voteshare.loc[geo][party] > 0:
                    out = polls_17[geo][party] / ge_2015_voteshare.loc[geo][party] - 1
                else:
                    out = 0.0
                swing_17.loc[geo, party] = out

        # Apply swing
        for party in parties_17:
            ge_2015[party + '_swing'] = ge_2015.apply(lambda row: swing_17.loc[row['geo']][party], axis=1)
            ge_2015[party + '_2017_forecast'] = ge_2015.apply(lambda x: x[party + '_pc'] * (1 + swing_17.loc[x['geo']][party]), axis=1)

        def win_17(row):
            return row[[p + '_2017_forecast' for p in parties_17]].sort_values(ascending=False).index[0].replace('_2017_forecast', '')

        ge_2015['win_17'] = ge_2015.apply(win_17, axis=1)

        ###########################
        # Create ML-ready dataframe
        ###########################

        parties = ['con', 'lab', 'ld', 'ukip', 'grn']
        act_15_lookup = {k: v for i, (k, v) in ge_2015[['Press Association ID Number', 'winner']].iterrows()}
        ge_2010['act_15'] = ge_2010['Press Association Reference'].map(act_15_lookup)
        pc_15_lookup = {
            p: {k: v for i, (k, v) in ge_2015[['Press Association ID Number', p + '_pc']].iterrows()} for p in parties
        }
        for p in parties:
            ge_2010[p + '_actual'] = ge_2010['Press Association Reference'].map(pc_15_lookup[p])

        df = ge_2010[['Press Association Reference', 'Constituency Name', 'Region', 'Electorate', 'Votes'] + parties]
        df = pd.melt(
            df,
            id_vars=['Press Association Reference', 'Constituency Name', 'Region', 'Electorate', 'Votes'],
            value_vars=parties,
            var_name='party',
            value_name='votes_last'
        )

        # pc_last
        pc_last = pd.melt(
            ge_2010[['Press Association Reference'] + [p + '_pc' for p in parties]],
            id_vars=['Press Association Reference'],
            value_vars=[p + '_pc' for p in parties],
            var_name='party',
            value_name='pc_last'
        )
        pc_last['party'] = pc_last.party.apply(lambda x: x.replace('_pc', ''))
        df = pd.merge(
            left=df,
            right=pc_last,
            how='left',
            on=['Press Association Reference', 'party']
        )

        # win_last
        win_last = ge_2010[['Press Association Reference', 'winner']]
        win_last.columns = ['Press Association Reference', 'win_last']
        df = pd.merge(
            left=df,
            right=win_last,
            on=['Press Association Reference']
        )

        # polls_now
        df['polls_now'] = df.party.map(polls['UK'])

        # swing_now
        swing_now = pd.melt(
            ge_2010[['Press Association Reference'] + [p + '_swing' for p in parties]],
            id_vars=['Press Association Reference'],
            value_vars=[p + '_swing' for p in parties],
            var_name='party',
            value_name='swing_now'
        )
        swing_now['party'] = swing_now.party.apply(lambda x: x.replace('_swing', ''))

        df = pd.merge(
            left=df,
            right=swing_now,
            how='left',
            on=['Press Association Reference', 'party']
        )

        # swing_forecast_pc
        swing_forecast_pc = pd.melt(
            ge_2010[['Press Association Reference'] + [p + '_forecast' for p in parties]],
            id_vars=['Press Association Reference'],
            value_vars=[p + '_forecast' for p in parties],
            var_name='party',
            value_name='swing_forecast_pc'
        )
        swing_forecast_pc['party'] = swing_forecast_pc.party.apply(lambda x: x.replace('_forecast', ''))

        df = pd.merge(
            left=df,
            right=swing_forecast_pc,
            how='left',
            on=['Press Association Reference', 'party']
        )

        # swing_forecast_win
        swing_forecast_win = ge_2010[['Press Association Reference', 'win_15']]
        swing_forecast_win.columns = ['Press Association Reference', 'swing_forecast_win']
        df = pd.merge(
            left=df,
            right=swing_forecast_win,
            on=['Press Association Reference']
        )

        # actual_win_now
        actual_win_now = ge_2010[['Press Association Reference', 'act_15']]
        actual_win_now.columns = ['Press Association Reference', 'actual_win_now']
        df = pd.merge(
            left=df,
            right=actual_win_now,
            on=['Press Association Reference']
        )

        # actual_pc_now
        actual_pc_now = pd.melt(
            ge_2010[['Press Association Reference'] + [p + '_actual' for p in parties]],
            id_vars=['Press Association Reference'],
            value_vars=[p + '_actual' for p in parties],
            var_name='party',
            value_name='actual_pc_now'
        )
        actual_pc_now['party'] = actual_pc_now.party.apply(lambda x: x.replace('_actual', ''))

        df = pd.merge(
            left=df,
            right=actual_pc_now,
            how='left',
            on=['Press Association Reference', 'party']
        )

        # dummy party
        df = pd.concat([df, pd.get_dummies(df.party)], axis=1)

        # dummy region
        df = pd.concat([df, pd.get_dummies(df.Region, prefix='Region')], axis=1)

        # won_here_last
        df['won_here_last'] = (df['party'] == df['win_last']).astype('int')

        # turnout
        df['turnout'] = df.Votes / df.Electorate

        ########################################
        # Export final 2010 -> 2015 training set
        ########################################
        print(f'Exporting 2010->2015 model dataset to {processed_directory.resolve()}')
        df.to_csv(processed_directory / 'general_election-uk-2015-model.csv', index=False)

        ######################
        # REPEAT FOR 2015-2017
        ######################
        # Recreate this training dataset using same column names for 2015 -> 2017 for a GE2017 forecast
        # TODO: Needs refactoring!
        # Add SNP and Plaid Cymru
        parties += ['snp', 'pc']
        df15 = ge_2015[['Press Association ID Number', 'Constituency Name', 'Region', 'geo', 'Electorate', 'Valid Votes'] + parties]
        df15.columns = ['Press Association ID Number', 'Constituency Name', 'Region', 'geo', 'Electorate', 'Votes'] + parties
        df15 = pd.melt(
            df15,
            id_vars=['Press Association ID Number', 'Constituency Name', 'Region', 'geo', 'Electorate', 'Votes'],
            value_vars=parties,
            var_name='party',
            value_name='votes_last'
        )

        # pc_last
        pc_last = pd.melt(
            ge_2015[['Press Association ID Number'] + [p + '_pc' for p in parties]],
            id_vars=['Press Association ID Number'],
            value_vars=[p + '_pc' for p in parties],
            var_name='party',
            value_name='pc_last'
        )
        pc_last['party'] = pc_last.party.apply(lambda x: x.replace('_pc', ''))

        df15 = pd.merge(
            left=df15,
            right=pc_last,
            how='left',
            on=['Press Association ID Number', 'party']
        )

        # win_last
        win_last = ge_2015[['Press Association ID Number', 'winner']]
        win_last.columns = ['Press Association ID Number', 'win_last']
        df15 = pd.merge(
            left=df15,
            right=win_last,
            on=['Press Association ID Number']
        )

        # polls_now <- USE REGIONAL POLLING! (Possibly a very bad idea, the regional UNS performed worse than national!)
        df15['polls_now'] = df15.apply(lambda row: polls_17[row.geo][row.party], axis=1)

        # swing_now
        swing_now = pd.melt(
            ge_2015[['Press Association ID Number'] + [p + '_swing' for p in parties]],
            id_vars=['Press Association ID Number'],
            value_vars=[p + '_swing' for p in parties],
            var_name='party',
            value_name='swing_now'
        )
        swing_now['party'] = swing_now.party.apply(lambda x: x.replace('_swing', ''))

        df15 = pd.merge(
            left=df15,
            right=swing_now,
            how='left',
            on=['Press Association ID Number', 'party']
        )

        # swing_forecast_pc
        swing_forecast_pc = pd.melt(
            ge_2015[['Press Association ID Number'] + [p + '_2017_forecast' for p in parties]],
            id_vars=['Press Association ID Number'],
            value_vars=[p + '_2017_forecast' for p in parties],
            var_name='party',
            value_name='swing_forecast_pc'
        )
        swing_forecast_pc['party'] = swing_forecast_pc.party.apply(lambda x: x.replace('_2017_forecast', ''))

        df15 = pd.merge(
            left=df15,
            right=swing_forecast_pc,
            how='left',
            on=['Press Association ID Number', 'party']
        )

        # swing_forecast_win
        swing_forecast_win = ge_2015[['Press Association ID Number', 'win_17']]
        swing_forecast_win.columns = ['Press Association ID Number', 'swing_forecast_win']
        df15 = pd.merge(
            left=df15,
            right=swing_forecast_win,
            on=['Press Association ID Number']
        )

        # dummy party
        df15 = pd.concat([df15, pd.get_dummies(df15.party)], axis=1)

        # dummy region
        df15 = pd.concat([df15, pd.get_dummies(df15.Region, prefix='Region')], axis=1)

        # won_here_last
        df15['won_here_last'] = (df15['party'] == df15['win_last']).astype('int')

        # turnout
        df15['turnout'] = df.Votes / df.Electorate

        ##########################################
        # Export final 2015 -> 2017 prediction set
        ##########################################
        print(f'Exporting 2015->2017 model dataset to {processed_directory.resolve()}')
        df15.to_csv(processed_directory / 'general_election-uk-2017-model.csv', index=False)
