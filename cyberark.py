import requests
import json

hostname = ""



class Cyberark(object):
    """

    """
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
        return cls.__instance

    def __init__(self):
        pass

    def authenticate_to_cyberark(self, username, password):
        self.rest_session = requests.Session()
        headers = {
            'Content-Type': 'application/json'
        }
        self.rest_session.verify = False
        self.base_url = "https://" + hostname + "/PasswordVault/API"
        logon_url = self.base_url + "/auth/LDAP/Logon"
        body = {"username": username, "password": password}
        payload = json.dumps(body)
        res = self.rest_session.post(url=logon_url, headers=headers, data=payload)
        if res.status_code == int('200'):
            headers['Authorization'] = res.text.strip('"')
            self.rest_session.headers = headers

    def get_account_details(self, acc_name):
        get_acc_det_url = self.base_url + "/Accounts?search=" + acc_name
        res = self.rest_session.get(url=get_acc_det_url, headers=self.rest_session.headers)
        print("Response code for account details: {}".format(res.status_code))
        return res.json()

    def get_password(self, acc_id):
        payload = "{reason:\"Retrieving from repository\"}"
        get_pwd_url = self.base_url + "/Accounts/" + acc_id + "/Password/Retrieve"
        res = self.rest_session.post(url=get_pwd_url, data=payload)
        print("Staus code for fetching password: {}".format(res.status_code))
        return res.text.strip('"')
