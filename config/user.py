class UserInfo:

    def __init__(self, user):
        self.user = user

    user_info = {'welly': {'username': 'welly',
                           'pwd': '10b2a52eb5e1702934e7e94c54d806fc6851aa1b'},
                 'welly1': {'username': 'welly1',
                            'pwd': 'ff9ff7ef892f14187c3dede2c848c94843e6e69e'},
                 'welly2': {'username': 'welly2',
                            'pwd': '3578165f887bbdf37a15e1e62c919e7471c73d1b'}}

    def username(self):
        return self.user_info[self.user]['username']

    def pwd(self):
        return self.user_info[self.user]['pwd']
