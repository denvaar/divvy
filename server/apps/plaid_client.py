import os
import requests


class PlaidClient(object):
    
    base_url = os.environ.get('PLAID_HOST', 'https://tartan.plaid.com')
    
    ENDPOINTS = {
        'institutions': '/institutions'
    }

    def __init__(self, client_id, secret, access_token=None):
        self.client_id = client_id
        self.secret = secret
        self.access_token = access_token

    def get_institutions(self, q=None, p=None):
        url = base_url + ENDPOINTS['institutions']
        response = requests.get(url)
