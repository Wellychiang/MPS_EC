import pytest
from pprint import pprint
import os
import allure
from base_api.base_players import Players, logger
from config.user import UserInfo
import subprocess


env = 'stg'
right_status = 200
wrong_status = 498
put_status = 204


def base_login_success(user='welly', status=right_status):
    player = Players(env)
    user_info = UserInfo(user)

    username = user_info.username()
    pwd = user_info.pwd()

    status_code, json = player.login(username, pwd)

    assert status_code == status
    assert json['needactivation'] is False
    assert json['verifytype'] == 'none'
    assert json['remaintime'] == -1
    assert json['token'] is not None
    assert json['settle'] is True


@allure.feature('Login')
@allure.story('Positive')
@allure.step('')
def test_login_success_with_three_user(names=['welly', 'welly1', 'welly2'], status=right_status):

    [base_login_success(name, status) for name in names]


@allure.feature('Login')
@allure.story('Minus')
@allure.step('')
def test_login_with_wrong_pwd(username='welly', pwd='asodijaosia', status=wrong_status):
    player = Players(env)
    status_code, json = player.login(username, pwd)

    assert status_code == status
    assert json['code'] == 2
    assert json['msg'] == 'userid or password is incorrect'
    assert json['replace'] is None


@allure.feature('Login')
@allure.story('Minus')
@allure.step('')
def test_login_with_username_unknown_input(usernames=['12345678901234', '叫我第一名', '!@#!*@&^#*'],
                                                  status=wrong_status):
    player = Players(env)
    for username in usernames:
        status_code, json = player.login(username)

        assert status_code == status
        assert json['code'] == 2
        assert json['msg'] == 'userid or password is incorrect'
        assert json['replace'] is None


@allure.feature('Login')
@allure.story('Minus')
@allure.step('')
def test_login_with_null_username(username=None, status=wrong_status):
    player = Players(env)
    status_code, json = player.login(username)

    assert status_code == status
    assert json['code'] == 0
    assert json['msg'] == 'Invalid param: loginname is empty'
    assert json['replace'] is None


@allure.feature('Login')
@allure.story('Minus')
@allure.step('')
def test_login_with_null_pwd(username='welly', pwd=None, status=wrong_status):
    player = Players(env)
    status_code, json = player.login(username, pwd)

    assert status_code == status
    assert json['code'] == 0
    assert json['msg'] == 'Invalid param: loginpassword is empty'
    assert json['replace'] is None


@allure.feature('Login')
@allure.story('Minus')
@allure.step('')
def test_login_with_null_username_and_pwd(username=None, pwd=None, status=wrong_status):
    player = Players(env)
    status_code, json = player.login(username, pwd)

    assert status_code == status
    assert json['code'] == 0
    assert json['msg'] == 'Invalid param: loginname is empty'
    assert json['replace'] is None


@allure.feature('Logout')
@allure.story('Positive')
@allure.step('')
def test_logout_success(status=put_status):
    player = Players(env)
    status_code = player.logout()

    assert status_code == status


def lookup_success(usernames, status):
    player = Players(env)

    for username in usernames:
        status_code, jsons = player.lookup(username)

        assert status_code == status
        for json in jsons:
            assert username in json


@allure.feature('Lookup')
@allure.story('Positive')
@allure.step('')
def test_lookup_success(usernames=['welly', 'wade', 'lily'], status=right_status):
    lookup_success(usernames, status)


@allure.feature('Lookup')
@allure.story('Minus')
@allure.step('')
def test_lookup_with_unknown_input(find_out_usernames=['asdz11ase', '!@#!@#!#@!@#', 'qw', ''], status=right_status):
    players = Players(env)

    for username in find_out_usernames:
        status_code, json = players.lookup(username)
        if username == find_out_usernames[0] or username == find_out_usernames[1]:
            assert status_code == status
            for j in json:
                assert j is None

        elif username == find_out_usernames[2] or username == find_out_usernames[3]:
            assert status_code == wrong_status
            assert json['code'] == 0
            assert json['msg'] == 'Invalid param: q should not be smaller than 3'

        else:
            raise ValueError('Do not input without arguments placeholder')


@allure.feature('Profile')
@allure.story('Minus')
@allure.step('')
def test_profile_with_hardcode(username='welly'):
    players = Players(env)
    userinfo = UserInfo(username)

    user = userinfo.username()
    pwd = userinfo.pwd()

    status_code, json = players.profile(user, pwd)
    json = json['player']

    assert json['playerid'] == username
    assert json['currency'] == 'CNY'
    assert json['firstname'] == username
    assert json['birthdate'] == 1034352000000
    assert json['birthday'] == 1034352000000
    assert json['mobile'] == '86 13131313131'
    assert json['im1'] is None
    assert json['im2'] is None
    assert json['tagnames'] is None
    assert json['affiliateid'] is None
    assert json['createdate'] == 1602475428095
    assert json['lastlogintime'] != 1603431826657
    assert json['internalplayer'] is False
    assert json['withdrawid']is None
    assert json['settle'] is True
    assert json['agentid'] is None
    assert json['pic1id'] is None
    assert json['pic2id'] is None
    assert json['pic1'] is None
    assert json['pic2'] is None
    assert json['hasverifiedmobile'] is False
    displayname = json['displayname']
    assert displayname['en-US'] == '青銅_English'
    assert displayname['hi-IN'] == '青銅_印度語'
    assert displayname['id-ID'] == '青銅_ndonesia'
    assert displayname['ja-JP'] == '青銅_日本語'
    assert displayname['ml-IN'] is None
    assert displayname['ms-MY'] == '青銅_Melayu'
    assert displayname['my-MM'] is None
    assert displayname['ta-IN'] is None
    assert displayname['th-TH'] == '青銅_ไทย'
    assert displayname['vi-VN'] == '青銅_Tiếng Việt'
    assert displayname['zh-CN'] == '青銅_簡體中文'
    assert displayname['zh-TW'] == '青銅_james'
    assert json['showforec'] is True
    assert json['ulagentid'] is None
    assert json['ulagentaccount'] is None


@allure.feature('Random')
@allure.story('Positive')
@allure.step('')
def test_random_success(methods=['get', 'post']):
    players = Players(env)

    for method in methods:
        status_code, json = players.random(method)

        assert json['uuid'] is not None
        assert json['image'] is not None


@allure.feature('Register')
@allure.story('Positive')
@allure.step('')
@pytest.mark.skip('Too much response to assert, do it later')
def test_register_setting():
    player = Players(env)
    status_code, json = player.register_setting()

    with open('register.json', 'r', encoding='utf-8') as f:
        for file in f:
            assert file == json


@allure.feature('Bank card setting')
@allure.story('Positive')
@allure.step('')
@pytest.mark.skip('Too much response to assert, do it later')
def test_bank_card_setting():
    player = Players(env)
    status_code, json = player.bank_card_setting()

    with open('rrrr.json', 'r', encoding='utf-8') as f:
        for file in f:
            file1 = file

    with open('trrrrr.json', 'r', encoding='utf-8') as f:
        for file in f:
            file2 = file

    import json
    from deepdiff import DeepDiff
    deep = DeepDiff(file1, file2)
    print(deep)


@allure.feature('Register')
@allure.story('Positive')
@allure.step('')
@pytest.mark.skip('Information is so less, do it later')
def test_register_isplayerinforready(username='welly1'):
    players = Players(env)
    userinfo = UserInfo(username)

    user = userinfo.username()
    pwd = userinfo.pwd()

    status_code, json = players.register_isplayerinforready(user, pwd)
    pprint(json)


@allure.feature('Register')
@allure.story('Positive')
@allure.step('')
@pytest.mark.skip('Wait for the DB Authority')
def test_register_success(user='welly', user_num=7, mobile_num=13131313138, status=right_status):
    players = Players(env)

    logger.info(f'\nnum: {user}{user_num}\nmobile_num: 86 {mobile_num}')
    status_code, json = players.register(user, user_num, mobile_num=mobile_num)

    while status_code != status:
        if json['msg'] == 'The specified playerid has been registered':
            user_num += 1
        elif json['msg'] == 'The specified mobile has been registered':
            mobile_num += 1

        status_code, json = players.register(user, user_num, mobile_num=mobile_num)

    logger.info(f'\nnum: {user}{user_num}\nmobile_num: 86 {mobile_num}')

    assert status_code == status
    assert json['needactivation'] is False
    assert json['verifytype'] == 'none'
    assert json['remaintime'] == -1
    assert json['token'] is not None
    assert json['settle'] is True


@allure.feature('Register')
@allure.story('Minus')
@allure.step('')
def test_register_with_same_playerid(user='welly', user_num=1, status=wrong_status):
    players = Players(env)
    status_code, json = players.register(user, user_num)

    assert status_code == status
    assert json['code'] == 2
    assert json['msg'] == 'The specified playerid has been registered'
    assert json['replace'] is None


@allure.feature('Register')
@allure.story('Minus')
@allure.step('')
def test_register_with_same_mobile_number(user='welly', user_num=1231, mobile_num=13131313131, status=wrong_status):
    players = Players(env)
    status_code, json = players.register(user, user_num, mobile_num)

    while json['msg'] == 'The specified playerid has been registered':
        user_num += 1

        if json['msg'] == 'The specified mobile has been registered':
            break

        status_code, json = players.register(user, user_num, mobile_num)

    assert status_code == status
    assert json['code'] == 4
    assert json['msg'] == 'The specified mobile has been registered'
    assert json['replace'] is None


@allure.feature('Register')
@allure.story('Minus')
@allure.step('')
@pytest.mark.skip('We do not have format judgment now')
def test_register_with_wrong_format_mobile_number(user='welly', user_num=1231, mobile_num=13131, status=wrong_status):
    players = Players(env)
    status_code, json = players.register(user, user_num, mobile_num)

    while json['msg'] == 'The specified playerid has been registered':
        user_num += 1

        if json['msg'] == 'The specified mobile has been registered':
            break

        status_code, json = players.register(user, user_num, mobile_num)

    assert status_code == status
    assert json['code'] == 4
    assert json['msg'] == 'The specified mobile has been registered'
    assert json['replace'] is None


@allure.feature('Login')
@allure.story('Positive')
@allure.step('')
@pytest.mark.skip('Not done and not found')
def test_ext_login():
    pass


@allure.feature('Reset')
@allure.story('Positive')
@allure.step('')
@pytest.mark.skip('Not done, options first , then put (payload need the encryption algorithm and args)')
def test_reset_password():
    pass


@allure.feature('Reset')
@allure.story('Positive')
@allure.step('')
@pytest.mark.skip('Not done, options first , then put (payload need the encryption algorithm and args) '
                  'and reset the fundpwd')
def test_pin():
    pass


@allure.feature('Profile')
@allure.story('Positive')
@allure.step('')
@pytest.mark.skip('Not done and not found')
def test_profile_settle():
    pass


@allure.feature('Profile')
@allure.story('Positive')
@allure.step('')
def test_profile_info(edit_title='firstname', edit_input='qqww', status=put_status):
    players = Players(env)
    status_code = players.profile_info(edit_title, edit_input)

    assert status_code == status


@allure.feature('Profile')
@allure.story('Minus')
@allure.step('')
def test_profile_info_with_invalid_mobile(edit_title='mobile', edit_input=2, mobile_input=132, status=wrong_status):
    players = Players(env)
    status_code, json = players.profile_info(edit_title, edit_input, mobile_input)

    assert status_code == status
    assert json['code'] == 0
    assert json['msg'] == 'Invalid param: mobile is empty'
    assert json['replace'] is None
    # {'code': 0, 'msg': 'Invalid param: mobile is empty', 'replace': None}
    # assert


if __name__ == '__main__':
    # pytest.main(['-vs', 'test_players.py::test_register_success'])

    # subprocess.call(['pytest', '-vs', 'test_players.py::test_profile_info'])

    os.system('del /q report')
    # subprocess.call(['pytest', '-vs', 'test_players.py::test_register_success', '--alluredir', 'report'])
    subprocess.call(['pytest', '-vs', '--alluredir', 'report'])
