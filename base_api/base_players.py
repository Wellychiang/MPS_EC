import requests
import logging
import sys
sys.path.append("..")
from config.url import Url
from urllib3 import encode_multipart_formdata

# a = 5

LOG_FILE_PATH = './log/Players.log'

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Log to screen
console_logger = logging.StreamHandler(sys.stdout)
logger.addHandler(console_logger)

# Log to file
file_logger = logging.FileHandler(LOG_FILE_PATH)
file_logger.setFormatter(formatter)
logger.addHandler(file_logger)


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
            "captchauuid": "799283eb-a54f-49b8-8fd1-f9d7d09d55ab",
            "fingerprint": "6d3c71dd5d7c436f33d505c9b94210f4",
            "loginname": username,
            "loginpassword": pwd,
            "portalid": "EC_DESKTOP"
        }

        r = self.s.post(url, headers=headers, json=data, verify=False)
        logger.info(f'username: {username}\nstatus code: {r.status_code}\nresponse: {r.json()}')

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
        logger.info(f'status code: {r.status_code}')

        return r.status_code

    # Done,
    # it's a verify feature about mouse leaving a register's input placeholder(It will show you all about your input)
    def lookup(self, valid_registers_username='welly'):
        site = Url(self.env)
        url = site.api_lookup()

        param = {'q': valid_registers_username}

        r = self.s.get(url, params=param, verify=False)
        logger.info(f'status code: {r.status_code}\nresponse: {r.json()}')
        return r.status_code, r.json()

    # Done, Refresh to get the personal profile(or money) (EC's money refresh button)
    def profile(self, username, pwd):
        site = Url(self.env)
        url = site.api_profile()

        _, login_token = self.login(username, pwd)
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
        logger.info(f'status code: {r.status_code}\nresponse: {r.json()}')
        return r.status_code, r.json()

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
        logger.info(f'status code: {r.status_code}\nresponse: {r.json()}')
        return r.status_code, r.json()

    # Not done yet, get register's setting's info
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
        logger.info(f'status code: {r.status_code}\nresponse: {r.json()}')
        return r.status_code, r.json()

    # Not done yet, get bankcard setting's info
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
        logger.info(f'status code: {r.status_code}\nresponse: {r.json()}')
        return r.status_code, r.json()

    # Not done yet
    def register_isplayerinforready(self, username, pwd):
        site = Url(self.env)
        url = site.api_register_isplayerinfoready()

        _, login_token = self.login(username, pwd)
        headers = {
                'Host': 'ae-api.stgdevops.site',
                'Connection': 'keep-alive',
                'Authorization': login_token['token'],
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/86.0.4240.111 Safari/537.36',
                'Accept': '*/*',
                'Origin': 'https://ae.stgdevops.site',
                'Sec-Fetch-Site': 'same-site',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Dest': 'empty',
                'Referer': 'https://ae.stgdevops.site/',
                'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7'
                }

        r = self.s.get(url, headers=headers)
        logger.info(f'status code: {r.status_code}\nresponse: {r.json()}')
        return r.status_code, r.json()

    def register(self, user='welly', user_num=5, mobile_num=13131313136, dieli=None):

        site = Url(self.env)
        url = site.api_register()

        headers = {
            'Host': 'ae-api.stgdevops.site',
            'Connection': 'keep-alive',
            'Content-Length': '1051',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/86.0.4240.111 Safari/537.36',
            'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundarytMpyO648AM9fjE8c',
            'Accept': '*/*',
            'Origin': 'https://ae.stgdevops.site',
            'Sec-Fetch-Site': 'same-site',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://ae.stgdevops.site/',
            'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',

        }

        data = {
            'playerid': (None, f'{user}{str(user_num)}'),
            'password': (None, 'fec5bf529c1ae70b2618b4d1db82b7135a7d371f'),
            'currency': (None, 'USD'),
            'mobile': (None, f'86 {str(mobile_num)}'),
            'portalid': (None, 'EC_DESKTOP'),
            'captcha': (None, '6876'),
            'captchauuid': (None, 'ae1dd0be-cba2-4ccc-a3e8-025911847ecc'),
            'regfingerprint': (None, '1435639e2a6a9da4eca32a98591390b3'),
            'language': (None, '2'),
        }

        if dieli == True:
            data['affiliateid'] = (None, 'CZHHBM')

        m = encode_multipart_formdata(data, boundary='----WebKitFormBoundarytMpyO648AM9fjE8c')

        r = self.s.post(url, headers=headers, data=m[0], verify=False)
        logger.info(f'status code: {r.status_code}\nresponse: {r.json()}')
        return r.status_code, r.json()


if __name__ == '__main__':
    players = Players()
    status, json = players.login()
    print(status, json)