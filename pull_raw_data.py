import os
import json
import requests
import math
import luigi
from luigi.contrib.s3 import AtomicS3File
import dask.bag as db

# raw data base endpoint
API_URL = 'http://api.reimaginebanking.com'

# api key for our "app"
with open('apikey') as f:
    API_KEY = f.read()

S3_BUCKET = 'evanfwelch-potamoi'
S3_PROJECT = 'production-feature-engineering'

DATA_PATH = './DATA'

class GetRawCustomerData(luigi.Task):
    """
    Makes API call for raw data
    """
    def requires(self):
        return None

    def output(self):
        return luigi.LocalTarget(os.path.join(DATA_PATH, 'RAW', 'customers.json'))

    def run(self):
        # call API
        r = requests.get(
            API_URL + '/customers',
            params={'key': API_KEY})

        # write the output to disk
        out_dir = os.path.dirname(self.output().path)
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)

        # write customer data
        with open(self.output().path, 'w') as f:
            json.dump(r.json(), f)

class GetRawAccountData(luigi.Task):

    def requires(self):
        None

    def output(self):
        return luigi.LocalTarget(os.path.join(DATA_PATH, 'RAW', 'accounts.json'))

    def run(self):
        # call API
        r = requests.get(
            API_URL + '/accounts',
            params={'key': API_KEY})

        if r.status_code != 200:
            print(r.status_code)
            print(r.url)
            raise Exception

        # write the output to disk
        out_dir = os.path.dirname(self.output().path)
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)

        with open(self.output().path, 'w') as f:
            json.dump(r.json(), f)

class GetRawTransactionData(luigi.Task):
    """
    Gets transactions for all customers
    """

    # how many partitions to talk about
    n_partitions = luigi.IntParameter(default=4)

    def requires(self):
        return GetRawAccountData()

    def output(self):
        return luigi.LocalTarget(
            os.path.join(
                DATA_PATH, 'RAW', 'purchases', 'manifest.json'))

    def run(self):

        # prepare output directory
        out_dir = os.path.dirname(self.output().path)
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)

        # read accounts data
        accounts_path = self.input().path
        with open(accounts_path, 'r') as af:
            d_acct = json.loads(af.read())


        cust_ids = list(set(map(lambda x: x['customer_id'], d_acct)))
        cust_ids.sort()

        # dict acct mapping -- could probably be ordered dict
        dict_cust_acct = {
            cust_id:
                list(map(lambda x: x['_id'],
                filter(lambda x: (x['customer_id'] == cust_id) &
                        (x['type'] == 'Credit Card'), d_acct)))
            for cust_id in cust_ids}

        file_cust_mapping = {}
        # custs per file
        rough_size = math.ceil(len(cust_ids)/self.n_partitions)
        for filenum in range(self.n_partitions):
            file_data = []
            file_cust_mapping[filenum] = []
            file_path = os.path.join(DATA_PATH, 'RAW', 'purchases',
                'purchase-{:04d}.json'.format(filenum))

            with open(file_path, 'w') as f:

                for cust in cust_ids[filenum*rough_size:(filenum+1)*rough_size]:
                    file_cust_mapping[filenum].append(cust)
                    for acct in dict_cust_acct[cust]:
                        print(acct)

                        # get this person's purchases
                        r = requests.get(
                            API_URL + '/accounts/{id}/purchases'.format(id=acct),
                            params={'key': API_KEY})

                        # fail legibly
                        if r.status_code != 200:
                            print(r.status_code)
                            print(r.url)
                            raise Exception

                        file_data.append(r.json())

                # write results to file
                json.dump(file_data, f)

        with open(self.output().path, 'w') as mani_f:
            json.dump(file_cust_mapping, mani_f)

class GetMerchantData(luigi.Task):
    # get all merchant info

    def requires(self):
        return None

    def output(self):
        out_path = os.path.join(
            DATA_PATH, 'RAW', 'merchant.json')

        return luigi.LocalTarget(out_path)

    def run(self):

        # get merchants from API
        r = requests.get(
            API_URL + '/merchants',
            params={'key': API_KEY})

        # write these records
        with open(self.output().path, 'w') as f:
            json.dump(r.json(), f)

class JoinAndFlattenTransactions(luigi.Task):
    # merge merchant and customer info into big flat table

    def requires(self):
        return {
            'merchant': GetMerchantData(),
            'transactions': GetRawTransactionData(),
            'customers': GetRawCustomerData(),
            'accounts': GetRawAccountData()}

    def output(self):
        output_pth = os.path.join(DATA_PATH, 'PROCESSED', 'enriched_trxns', 'manifest.touch')
        return luigi.LocalTarget(output_pth)

    def run(self):

        # get transactions bag
        trxn_glob = os.path.dirname(self.requires()['transactions'].output().path)
        trxn_glob = os.path.join(trxn_glob, 'purchase-*.json')

        # get transactions bag
        trxn_bag = db.read_text(trxn_glob).map(json.loads).flatten().flatten()

        # load cust data
        cust_file = self.requires()['customers'].output().path
        with open(cust_file, 'r') as cust_f:
            custs = json.loads(cust_f.read())
        cust_key = {cust['_id']: cust for cust in custs}

        # load account data
        acct_file = self.requires()['accounts'].output().path
        with open(acct_file, 'r') as acct_f:
            accts = json.loads(acct_f.read())
            print(len(accts))
        acct_cust_key = {acct['_id']:acct['customer_id'] for acct in accts}
        acct_rewards_key = {acct['_id']:acct['rewards'] for acct in accts}

        # load merchant data
        mrch_file = self.requires()['merchant'].output().path
        with open(mrch_file, 'r') as mrch_f:
            merchants = json.loads(mrch_f.read())
        mrch_key = {mrch['_id']: mrch for mrch in merchants}


        def _enrich_trxn(trxn, cust_key, acct_cust_key, acct_rewards_key, mrch_key):
            new_trxn = {**trxn}

            # account details
            new_trxn['customer_id'] = acct_cust_key[trxn['payer_id']]
            new_trxn['rewards'] = acct_rewards_key[trxn['payer_id']]

            # customer details
            new_trxn['cust_first_nm'] = cust_key[new_trxn['customer_id']]['first_name']
            new_trxn['cust_last_nm'] = cust_key[new_trxn['customer_id']]['last_name']
            new_trxn['cust_state'] = cust_key[new_trxn['customer_id']]['address']['state']
            new_trxn['cust_zip'] = cust_key[new_trxn['customer_id']]['address']['zip']

            # relevant merchant
            this_mrch = mrch_key[trxn['merchant_id']]

            # merchant addr
            this_addr = this_mrch.get('address', {})
            new_trxn['mrch_state'] = this_addr.get('state', None)
            new_trxn['mrch_zip'] = this_addr.get('zip', None)

            # merchant lat/oon
            this_geo = this_mrch.get('geocode', {})
            new_trxn['mrch_lat'] = this_geo.get('lat', None)
            new_trxn['mrch_lon'] = this_geo.get('lon', None)

            # merchant categories
            new_trxn['mrch_catgs'] = this_mrch.get('category',[])

            return new_trxn

        enriched_trxns = trxn_bag.map(lambda trxn: _enrich_trxn(trxn,
            cust_key=cust_key,
            acct_cust_key=acct_cust_key,
            acct_rewards_key=acct_rewards_key,
            mrch_key=mrch_key))

        ddf = enriched_trxns.to_dataframe()

        # write this to file
        out_dir = os.path.join(DATA_PATH, 'PROCESSED', 'enriched_trxns', 'enriched_trxns-*.csv')
        if not os.path.exists(os.path.dirname(out_dir)):
            os.makedirs(os.path.dirname(out_dir))

        # publish this data
        ddf.to_csv(
            out_dir,
            sep='|',
            index=False,
            chunksize=5)
