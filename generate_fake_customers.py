import os
import requests
import json
from faker import Faker
import numpy as np

# fake data utility
fake = Faker()

# get the apikey
PATH_API_KEY = os.path.join(os.path.dirname(os.path.abspath(__file__)),'apikey')
with open(PATH_API_KEY, 'r') as api_f:
    api_key = api_f.read()

# reusable params
PARAMS = {'key': api_key}

# some stubs for calling hte API
ROOT_URL = 'http://api.reimaginebanking.com/data'
API_URL = 'http://api.reimaginebanking.com'
URL = 'http://api.reimaginebanking.com/customers?key={}'.format(api_key)

# how many customers to generate
N_CUSTOMERS = 10

def new_customer_payload():
    new_cust = {}
    new_cust['first_name'] = fake.first_name()
    new_cust['last_name'] = fake.last_name()

    new_addr = {
        'street_number': fake.building_number(),
        'street_name': fake.street_name(),
        'city': fake.city(),
        'state': fake.state_abbr(),
        'zip': fake.zipcode()}

    new_cust['address'] = new_addr
    return new_cust

def remove_customers():
    params={'key': api_key, 'type': 'Customers'}
    r = requests.delete(
        ROOT_URL,
        params=params,
        headers={'Accept': 'application/json'})

    if r.status_code == 404:
        resp = r.json()
        if resp['message'] != 'No data to delete':
            raise Exception(r.json())

def add_customers(n=N_CUSTOMERS):

    for _ in range(n):
        r = requests.post(
            URL,
            data=json.dumps(new_customer_payload()),
            headers={'content-type':'application/json'})

        if r.status_code != 201:
            print(r.text)
            raise

def get_customers():

    r = requests.get(API_URL + '/customers', params={'key': api_key})
    return r.json()

def generate_card():

    card_dict = {
        'type': 'Credit Card',
        'nickname': fake.word(),
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

if __name__ == '__main__':
    # get rid of customers
    remove_customers()
    # add customers
    add_customers()
    # get those added custs
    custs = get_customers()
    # make cc accounts
    add_customer_cards(custs)
    # get those accts
    accts, acct_by_cust = get_all_accounts()
