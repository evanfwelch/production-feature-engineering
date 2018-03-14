import os
from faker import Faker

# fake data utility
FAKE = Faker()


# get the apikey
PATH_API_KEY = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), '..', 'apikey')

with open(PATH_API_KEY, 'r') as api_f:
    API_KEY = api_f.read()

# reusable params
PARAMS = {'key': API_KEY}

# URL STUB
API_URL = 'http://api.reimaginebanking.com'
