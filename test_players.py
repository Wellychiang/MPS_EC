import pytest
from pprint import pprint
import pytest_check as check
import os
import allure
from base_api.base_players import Players, logger
from config.user import UserInfo
import subprocess


env = 'stg'
right_status = 200
wrong_status = 498


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
    assert '' not in json['token']
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
def test_logout_success(status=204):
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
def test_lookup_with_unknown_input(find_out_usernames=['asdz11ase', '!@#!@#!#@!@#', 'qw'], status=right_status):
    players = Players(env)

    for username in find_out_usernames:
        status_code, json = players.lookup(username)
        if username == find_out_usernames[0] or username == find_out_usernames[1]:
            check.equal(status_code, status)
            for j in json:
                assert j is None

        elif username == find_out_usernames[2]:
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
    assert json['createdate'] is 1602475428095
    assert json['lastlogintime'] != 1603431826657
    assert json['internalplayer'], False
    assert json['withdrawid'], None
    assert json['settle'], True
    assert json['agentid'], None
    assert json['pic1id'], None
    assert json['pic2id'], None
    assert json['pic1'], None
    assert json['pic2'], None
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


# It's too much to assert, do it later
def test_register_setting():
    player = Players(env)
    status_code, json = player.register_setting()

    with open('register.json', 'r', encoding='utf-8') as f:
        for file in f:
            assert file == json


# It's too much to assert, do it later
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


# Information is too less
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


if __name__ == '__main__':
    # pytest.main(['-vs', 'test_players.py::test_register_success'])

    # subprocess.call(['pytest', '-vs', 'test_players.py::test_register_with_same_mobile_number'])
    #
    os.system('del /q report')
    # pytest.main(['-vs', '--alluredir', 'report'])
    subprocess.call(['pytest', '-vs', 'test_players.py::test_register_with_same_mobile_number', '--alluredir', 'report'])
