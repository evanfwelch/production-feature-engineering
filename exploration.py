"""
Makes all the features in the notebook
"""
import os
import dask.dataframe as dd
from distributed import Client
import datetime
import pandas as pd
import numpy as np

# source data path
ENRICHED_TRXN_DATA = './DATA/PROCESSED/enriched_trxns/enriched_trxns-*.csv'
# where to save features
FEATURE_PATH = 'DATA/FEATURES/'

# make dir if not exists
if not os.path.exists(FEATURE_PATH):
    os.makedirs(FEATURE_PATH)


# filter functions
def no_rewards_purchases(trxn):
    return trxn['medium'] != 'reward'

def only_this_catg(trxn, catg):
    return any([catg.lower() in cat.lower() for cat in trxn['mrch_catgs'].split()])

def only_this_date(trxn, year=None, month=None, day=None):
    result = True
    try:
        trxn_dt = pd.to_datetime(trxn['purchase_date'])
    except:
        trxn_dt = pd.NaT
    if year:
        result &= trxn_dt.year == year
    if month:
        result &= trxn_dt.month == month
    if day:
        result &= trxn_dt.day == day

    return result



# ## some new columns
def first_digit_zip_code(zip_str):
    if len(zip_str) >= 5:
        return int(zip_str[0])
    else:
        return np.nan

def is_amazon(trxn):
    return 'amazon' in trxn['mrch_name'].lower()


# aggregation functions
def _trxn_cnt(df):
    return df.shape[0]

def _trxn_total(df):
    return df['amount'].sum()

def _trxn_mean(df):
    return df['amount'].mean()

agg_operations = {
    'cnt': _trxn_cnt,
    'tot': _trxn_total,
    'avg': _trxn_mean}

# workhorse function that saves series to disk
def write_feature(srs, feat_path):
    feature_folder = os.path.join(FEATURE_PATH, feat_path)
    if not os.path.exists(feature_folder):
        os.makedirs(feature_folder)

    # write the feature to disk
    files = srs.to_csv(os.path.join(FEATURE_PATH, feat_path, 'part-*.csv'), sep='|', index_label='customer_id')
    return files


def generate_features(ddf):
    catgories_of_interest = ['grocery', 'food', 'bar']
    dates = pd.date_range('2017-12-01', '2017-12-10')

    for catg in catgories_of_interest:
        for dt in dates:

            # apply filters
            keep_rows = (
                    ddf.apply(no_rewards_purchases, axis=1) &
                    ddf.apply(lambda row: only_this_catg(row, catg=catg), axis=1) &
                    ddf.apply(lambda row: only_this_date(row, year=dt.year, month=dt.month, day=dt.day), axis=1))

            # prepare for aggregate functions
            g = ddf.loc[keep_rows, :].groupby('customer_id')

            feat_path_template = '{dt}/{catg}_{op}'

            for agg_name, agg_func in agg_operations.items():
                feat_path = feat_path_template.format(
                    dt=dt.strftime('%Y%m%d'),
                    catg=catg,
                    op=agg_name)

                # write the feature to disk
                write_feature(g.apply(agg_func), feat_path)

                # print result
                print("Wrote feature: {}".format(feat_path))

def read_data():
    # using dask dataframes, very similar to pandas
    ddf = dd.read_csv(ENRICHED_TRXN_DATA, sep='|', dtype={'mrch_zip':str, 'zip': str})
    return ddf
    
if __name__ == '__main__':

    clt = Client('localhost:8786')

    # using dask dataframes, very similar to pandas
    ddf = dd.read_csv(ENRICHED_TRXN_DATA, sep='|', dtype={'mrch_zip':str, 'zip': str})
    generate_features(ddf)
