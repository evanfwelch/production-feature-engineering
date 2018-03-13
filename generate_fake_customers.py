import os
import requests
import json
from faker import Faker
import numpy as np

fake = Faker()

# get the apikey
PATH_API_KEY = os.path.join(os.path.dirname(os.path.abspath(__file__)),'apikey')
with open(PATH_API_KEY, 'r') as api_f:
    api_key = api_f.read()

PARAMS = {'key': api_key}

ROOT_URL = 'http://api.reimaginebanking.com/data'
API_URL = 'http://api.reimaginebanking.com'
URL = 'http://api.reimaginebanking.com/customers?key={}'.format(api_key)


N_CUSTOMERS = 1000

# delete customers

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

def add_customer_cards(lst_customers):

    for cust in lst_customers:
        # how many credit cards to give this customer
        n_cards = np.random.randint(3)

        # create credit card account

def get_accounts():
    raise NotImplementedError

def generate_transaction(datetime):
    raise NotImplementedError

def add_transactions(lst_accounts):
    raise NotImplementedError


if __name__ == '__main__':
    # r = remove_customers()
    # add_customers(1000)
    print(get_customers())
