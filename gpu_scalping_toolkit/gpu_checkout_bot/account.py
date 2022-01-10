from enum import Enum


class ACCOUNT_REGION(Enum):
    DMV = 1
    ATL = 2
    SF = 3


class AccountDTO:
    def __init__(self, email: str, gmail_password: str, bestbuy_password: str, mfa_token: str,
                 region: ACCOUNT_REGION, proxy_user: str, proxy_password, proxy_host: str, proxy_port: int):
        self.email = email
        self.gmail_password = gmail_password
        self.bestbuy_password = bestbuy_password
        self.mfa_token = mfa_token
        self.region = region
        self.proxy_user = proxy_user
        self.proxy_password = proxy_password
        self.proxy_host = proxy_host
        self.proxy_port = proxy_port

    def __str__(self):
        return f'''
            {{
                "email": {self.email},
                "gmail_password": {self.gmail_password},
                "bestbuy_password": {self.bestbuy_password},
                "mfa_token": {self.mfa_token},
                "region": {self.region},
                "proxy_user": {self.proxy_user},
                "proxy_password": {self.proxy_password},
                "proxy_host": {self.proxy_host},
                "proxy_port": {self.proxy_port}
            }}
        '''
