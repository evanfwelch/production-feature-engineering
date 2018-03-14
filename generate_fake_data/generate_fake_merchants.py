# """
# This module creates an ecosystem of fake merchants
# """
# import os
# import csv
# import pandas as pd
# from .utils import API_URL
#
# # where to find business datasets
# MERCHANT_DATA_PATH = os.path.join(
#     os.path.dirname(os.path.abspath(__file__)), '..', 'merchant_data')
#
#
# # def format_merchant_record(row):
# #     record = {}
# #     record['name'] = row['name']
# #     record['category'] = row['categories']
# #     record['address'] = {
# #         'street_number': row['address'].split()[0],
# #         'street_name': ' '.join(row['address'].split()[1:]),
# #         'city': row['city'],
# #         'state': row['state'],
# #         'zip': row['postal_code']}
# #     record['geocode'] = {
# #         'lat': row['latitude'],
# #         'lng': row['longitude']}
# #
# #     return record
# #
# # def delete_merchants():
# #     r = requests.delete(API_URL + '/data',
# #         params={'key': API_KEY, 'type': 'Merchants'})
# #
# #     if r.status_code != 201:
# #         print(r.status_code)
# #         print(r.url)
# #         print(r.text)
#
# # def load_merchants():
# #     """
# #     Parses the Yelp dataset and creates merchants in our DB.
# #     """
# #
# #     # data path
# #     data_path = os.path.join(MERCHANT_DATA_PATH, 'yelp_business.csv')
# #
# #     # dict reader
# #     with open(data_path, 'r') as bf:
# #
# #         # get header
# #         header = bf.readline().strip().split(';')
# #         # dict reader
# #         d_reader = csv.DictReader(bf, fieldnames=header)
# #
# #         for row in d_reader:
# #
# #             # get record
# #             rec = format_merchant_record(row)
# #
# #             # this url
# #             r = requests.post(
# #                 API_URL + '/merchants'
# #                 PARAMS=PARAMS,
# #                 headers={'content-type': 'application/json'},
# #                 data=json.dumps(rec))
# #
# #             if r.status_code != 201:
# #                 print(r.status_code)
# #                 print(r.url)
# #                 raise
# #
# #
# #
#
#
#
#
#
# if __name__ == '__main__':
#     # clear old merchants
#     delete_merchants()
#
#     # upload merch
#     load_merchants()
