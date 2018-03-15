import os
import requests
import json
import numpy as np
import pandas as pd

#### UTILITIES #########
# from .utils import FAKE, PARAMS, API_KEY, API_URL
from faker import Faker
# fake data utility
FAKE = Faker()
# get the apikey
PATH_API_KEY = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),  'apikey')
with open(PATH_API_KEY, 'r') as api_f:
    API_KEY = api_f.read()
# reusable params
PARAMS = {'key': API_KEY}
# URL STUB
API_URL = 'http://api.reimaginebanking.com'
#############

# how many customers to generate
N_CUSTOMERS = 1000

def new_customer_payload():
    new_cust = {}
    new_cust['first_name'] = FAKE.first_name()
    new_cust['last_name'] = FAKE.last_name()

    new_addr = {
        'street_number': FAKE.building_number(),
        'street_name': FAKE.street_name(),
        'city': FAKE.city(),
        'state': FAKE.state_abbr(),
        'zip': FAKE.zipcode()}

    new_cust['address'] = new_addr
    return new_cust

def remove_customers():
    params={'key': API_KEY, 'type': 'Customers'}
    r = requests.delete(
        API_URL + '/data',
        params=params,
        headers={'Accept': 'application/json'})

    if r.status_code == 404:
        resp = r.json()
        if resp['message'] != 'No data to delete':
            raise Exception(r.json())

def remove_accounts():
    params={'key': API_KEY, 'type': 'Accounts'}
    r = requests.delete(
        API_URL + '/data',
        params=params,
        headers={'Accept': 'application/json'})

    if r.status_code == 404:
        resp = r.json()
        if resp['message'] != 'No data to delete':
            raise Exception(r.json())

def add_customers(n=N_CUSTOMERS):

    for _ in range(n):
        r = requests.post(
            API_URL + '/customers',
            params=PARAMS,
            data=json.dumps(new_customer_payload()),
            headers={'content-type':'application/json'})

        if r.status_code != 201:
            print(r.url)
            raise

def get_customers():

    r = requests.get(API_URL + '/customers', params={'key': API_KEY})
    return r.json()

def generate_card():

    card_dict = {
        'type': 'Credit Card',
        'nickname': FAKE.word(),
        'rewards': 0,
        'balance': 0}
    return card_dict


def add_customer_cards(lst_customers):
    """
    Create card accounts for these customers
    """
    for cust in lst_customers:

        this_url = API_URL + '/customers/{id}/accounts'.format(id=cust['_id'])

        # how many credit cards to give this customer
        n_cards = np.random.randint(1,4)

        for _ in range(n_cards):
            # get new credit card
            new_card = generate_card()

            # add it
            r = requests.post(
                this_url,
                headers={
                    'Content-type': 'application/json',
                    'Accept': 'application/json'},
                data=json.dumps(new_card),
                params=PARAMS)

def get_all_accounts():
    # get this url
    this_url = API_URL + '/accounts'

    # call API
    r = requests.get(this_url,
        headers={'Accept': 'application/json'},
        params=PARAMS)

    # get acct details
    acct_details = r.json()

    # also by cust
    acct_by_cust = {}
    for acct in acct_details:
        # extract
        cust_id = acct['customer_id']
        acct_id = acct['_id']

        # deal with this cust
        if cust_id not in acct_by_cust:
            acct_by_cust[cust_id] = []

        acct_by_cust[cust_id].append(acct_id)
    return acct_details, acct_by_cust

def get_merchants():

    r = requests.get(API_URL + '/merchants', params=PARAMS)
    return r.json()

def remove_transactions():
    r = requests.delete(API_URL + '/data', params={'key': API_KEY, 'type': 'Purchases'})

def generate_transactions(custs, acct_by_cust, merchants):

    # range of dates
    dates = pd.date_range('2017-12-01', '2017-12-10')

    # customer persona definitions
    # categories
    categories = ['gas', 'grocery', 'bar', 'liquor', 'clothing', 'shopping', 'travel', 'lodging']
    eligible_merchants = {catg: [] for catg in categories}

    for merch in merchants:
        for merch_cat in merch['category']:
            for catg in categories:
                if catg.lower() in merch_cat.lower():
                    eligible_merchants[catg].append(merch['_id'])

    average_spend = [50, 80, 25, 35, 79, 22, 450, 250]
    persona_probs = {
        'routine': [50, 60, 15, 5, 8, 15, 1, 3],
        'traveler': [4, 4, 30, 5, 15, 35, 25, 35],
        'shopper': [4, 10, 20, 8, 33, 45, 10, 10]}

    purchase_freq = {
        'routine': 1,
        'traveler': .3,
        'shopper': .7
    }

    # purch_url
    purchase_url = API_URL + '/accounts/{id}/purchases'
    # loop over customers
    for cust in custs:
        trxn_cnt = 0
        # pick customer persona
        cust_type = np.random.choice(['routine', 'traveler', 'shopper'])

        for dt in dates:

            # if theres a purchase today
            val = np.random.rand()
            if val <= purchase_freq[cust_type]:

                # get account number
                this_acct = np.random.choice(acct_by_cust[cust['_id']])
                # this_acct = acct_by_cust[cust][0]

                # choose cat
                catg = np.random.choice(categories, p=[pr/sum(persona_probs[cust_type]) for pr in persona_probs[cust_type]])
                idx = categories.index(catg)

                if eligible_merchants[catg]:
                    merch_id = np.random.choice(eligible_merchants[catg])

                    # make trxn
                    r = requests.post(
                        purchase_url.format(id=this_acct),
                        headers={'Content-type': 'application/json'},
                        data=json.dumps({
                            'merchant_id': merch_id,
                            'medium': 'balance',
                            'purchase_date': dt.date().strftime('%Y-%m-%d'),
                            'amount': average_spend[idx]*(.5+ np.random.rand()),
                            'status': 'completed'
                        }),
                        params=PARAMS)


                    if r.status_code != 201:
                        print(r.status_code)
                        print(r.url)
                        raise
                    else:
                        trxn_cnt += 1
        print("generated {} transactions for customer's acct {}".format(
            str(trxn_cnt), this_acct))


if __name__ == '__main__':
    # get rid of customers
    remove_customers()
    # add customers
    add_customers()
    # get those added custs
    custs = get_customers()

    # make cc accounts
    remove_accounts()
    add_customer_cards(custs)

    # get those accts
    accts, acct_by_cust = get_all_accounts()

    # get the global list of merchants
    lst_merch = get_merchants()

    # make the transactions finally
    remove_transactions()
    generate_transactions(custs, acct_by_cust, lst_merch)
