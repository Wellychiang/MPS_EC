class Url:

    def __init__(self, site):
        self.site = site
    stg = 'https://ae-api.stgdevops.site/ae-ecp/api/v1/'
    pro = 'https://api.ae1888.com/ae-ecp/api/v1/'

    # Players
    _sync = 'sync'
    _login = 'login'
    _logout = 'logout'
    _lookup = 'players/lookup'
    _profile = 'profile'
    _wallets = 'wallets'
    _random = 'captchas/random'
    _register_setting = 'register/setting'
    _bankcard_setting = 'bankcard/setting'
    _register_isplayerinfoready = 'register/isplayerinfoready'
    _register = 'register'
    _ext_login = 'ext/login'

    sync = {'stg': stg + _sync,
            'pro': pro + _sync}
    login = {'stg': stg + _login,
             'pro': pro + _login}
    logout = {'stg': stg + _logout,
              'pro': pro + _logout}
    lookup = {'stg': stg + _lookup,
              'pro': pro + _lookup}
    profile = {'stg': stg + _profile,
               'pro': pro + _profile}
    random = {'stg': stg + _random,
              'pro': pro + _random}
    register_setting = {'stg': stg + _register_setting,
                        'pro': pro + _register_setting}
    bankcard_setting = {'stg': stg + _bankcard_setting,
                        'pro': pro + _bankcard_setting}
    register_isplayerinfoready = {'stg': stg + _register_isplayerinfoready,
                                  'pro': pro + _register_isplayerinfoready}
    register = {'stg': stg + _register,
                'pro': pro + _register}
    ext_login = {'stg': stg + _ext_login,
                 'pro': pro + _ext_login}
    # random = {'stg': stg + _random,
    #           'pro': pro + _random}
    # random = {'stg': stg + _random,
    #           'pro': pro + _random}
    # random = {'stg': stg + _random,
    #           'pro': pro + _random}
    # random = {'stg': stg + _random,
    #           'pro': pro + _random}
    # random = {'stg': stg + _random,
    #           'pro': pro + _random}
    # random = {'stg': stg + _random,
    #           'pro': pro + _random}

    def api_sync(self):
        return self.sync[self.site]

    def api_login(self):
        return self.login[self.site]

    def api_logout(self):
        return self.logout[self.site]

    def api_lookup(self):
        return self.lookup[self.site]

    def api_profile(self):
        return self.profile[self.site]

    def api_random(self):
        return self.random[self.site]

    def api_register_setting(self):
        return self.register_setting[self.site]

    def api_bankcard_setting(self):
        return self.bankcard_setting[self.site]

    def api_register_isplayerinfoready(self):
        return self.register_isplayerinfoready[self.site]

    def api_register(self):
        return self.register[self.site]

    def api_ext_login(self):
        return self.ext_login[self.site]

