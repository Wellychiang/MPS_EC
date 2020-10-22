import requests
import logging
import sys
sys.path.append("..")
from config.url import Url


logging.basicConfig(level=logging.INFO, filename='../Players.log',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


class Players:

    s = requests.session()

    def __init__(self, env='stg'):
        self.env = env
        if env == 'stg' or env == 'pro':
            pass
        else:
            raise ValueError('Please input the correct env, like stg or pro')

    # Not done(needs header) (this api is trivial api to extend token time)
    def sync(self):
        site = Url(self.env)
        url = site.api_sync()

        _, login_token = self.login()
        headers = {
            'Accept': '*/*',
            'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'Authorization': login_token['token'],
            'Connection': 'keep-alive',
            'Host': 'ae-api.stgdevops.site',
            'Origin': 'https://ae.stgdevops.site',
            'Referer': 'https://ae.stgdevops.site/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0'
                          '.4240.75 Safari/537.36'
        }
        r = self.s.get(url, headers=headers)
        print(r.json())

    # Done
    def login(self, username='welly', pwd='10b2a52eb5e1702934e7e94c54d806fc6851aa1b'):
        site = Url(self.env)
        url = site.api_login()

        headers = {
            'Host': 'ae-api.stgdevops.site',
            'Connection': 'keep-alive',
            'Content-Length': '223',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36',
            'Content-Type': 'application/json;charset=UTF-8',
            'Accept': '*/*',
            'Origin': 'https://ae.stgdevops.site',
            'Sec-Fetch-Site': 'same-site',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://ae.stgdevops.site/',
            # 'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7'
        }

        data = {
            "captcha": "9999",
            "captchauuid": "90b70885-535f-4018-8800-e8022cc747d9",
            "fingerprint": "6eedcdae98a1f29eeab414a9ce79f2be",
            "loginname": username,
            "loginpassword": pwd,
            "portalid": "EC_DESKTOP"
        }

        r = self.s.post(url, headers=headers, json=data, verify=False)
        print(r.json(), r.status_code)
        return r.status_code, r.json()

    # Done, expected 204
    def logout(self):
        site = Url(self.env)
        url = site.api_logout()

        _, login_token = self.login()
        headers = {
            'Host': 'ae-api.stgdevops.site',
            'Connection': 'keep-alive',
            'Content-Length': '0',
            'Authorization': login_token['token'],
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/86.0.4240.75 Safari/537.36',
            'Content-Type': 'application/json;charset=UTF-8',
            'Accept': '*/*',
            'Origin': 'https://ae.stgdevops.site',
            'Sec-Fetch-Site': 'same-site',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://ae.stgdevops.site/',
            'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7'
                    }

        r = self.s.put(url, headers=headers, verify=False)
        print(r.status_code, r.text)
        return r.status_code, r.json()

    # it's a verify feature about mouse leaving a register's input placeholder
    def lookup(self, valid_registers_username='lily'):
        site = Url(self.env)
        url = site.api_lookup()

        param = {'q': valid_registers_username}
        r = self.s.get(url, params=param, verify=False)
        print(r.status_code, r.json())

    # Done, Refresh to get the personal profile(or money) (EC's money refresh button)
    def profile(self):
        site = Url(self.env)
        url = site.api_profile()

        _, login_token = self.login()
        headers = {
            'Accept': '*/*',
            'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'Authorization': login_token['token'],
            'Connection': 'keep-alive',
            'Host': 'ae-api.stgdevops.site',
            'Origin': 'https://ae.stgdevops.site',
            'Referer': 'https://ae.stgdevops.site/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0'
                          '.4240.75 Safari/537.36'
        }

        r = self.s.get(url, headers=headers)
        print(r.json(), r.headers)

    # Done, Generate a random captcha(need to verify post and get both)
    def random(self, method='get'):
        site = Url(self.env)
        url = site.api_random()

        if method == 'get':
            r = self.s.get(url, verify=False)
        elif method == 'post':
            r = self.s.post(url, verify=False)
        else:
            raise ValueError('Please input the right method, like post or get')
        logging.info(r.json())
        print(r.json())
        return r.status_code, r.json()

    # Done, get register's setting's info
    def register_setting(self):
        site = Url(self.env)
        url = site.api_register_setting()

        _, login_token = self.login()
        headers = {
            'Accept': '*/*',
            'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'Authorization': login_token['token'],
            'Connection': 'keep-alive',
            'Host': 'ae-api.stgdevops.site',
            'Origin': 'https://ae.stgdevops.site',
            'Referer': 'https://ae.stgdevops.site/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0'
                          '.4240.75 Safari/537.36'
        }

        r = self.s.get(url, headers=headers)
        print(r.json())
        return r.json()

    # Done, get bankcard setting's info
    def bank_card_setting(self):
        site = Url(self.env)
        url = site.api_bankcard_setting()

        _, login_token = self.login()
        headers = {
            'Accept': '*/*',
            'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'Authorization': login_token['token'],
            'Connection': 'keep-alive',
            'Host': 'ae-api.stgdevops.site',
            'Origin': 'https://ae.stgdevops.site',
            'Referer': 'https://ae.stgdevops.site/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0'
                          '.4240.75 Safari/537.36'
        }

        r = self.s.get(url, headers=headers)
        print(r.json())
        return r.json()


# if __name__ == '__main__':
#
#     players = Players('stg')
#     players.login()




