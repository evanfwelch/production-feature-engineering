import os
import requests
import json

customerId = 'your customerId here'

# get the apikey
PATH_API_KEY = os.path.join(os.path.dirname(os.path.abspath(__file__)),'apikey')
with open(PATH_API_KEY, 'r') as api_f:
    api_key = api_f.read()

print(api_key)
URL = 'http://api.reimaginebanking.com/customers?key={}'.format(api_key)

response = requests.get(URL, headers={'Accept':'application/json'})

if __name__ == '__main__':
    print(response)
    print(response.text)

# payload = {
#   "type": "Savings",
#   "nickname": "test",
#   "rewards": 10000,
#   "balance": 10000,
# }
# # Create a Savings Account
# response = requests.post(
# 	url,
# 	data=json.dumps(payload),
# 	,
# 	)
#
# if response.status_code == 201:
# 	print('account created')
