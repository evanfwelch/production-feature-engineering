"""
This module creates an ecosystem of fake merchants
"""
import os
import csv
import pandas as pd


# where to find business datasets
MERCHANT_DATA_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'merchant_data')

def get_merchant_data():

    # data path
    data_path = os.path.join(MERCHANT_DATA_PATH, 'yelp_business.csv')

    # dict reader
    with open(data_path, 'r') as bf:

        header = bf.readline()
        d_reader = csv.DictReader()





if __name__ == '__main__':

    #
    biz_path = os.path.join(MERCHANT_DATA_PATH, 'yelp_business.csv')

    # get data
    df_merch = pd.read_csv(
        biz_path,
        sep=',')

    print(df_merch.head())
    print(df_merch.shape)
