import pytest
from pprint import pprint
import pytest_check as check
import os
import allure
from base_api.base_players import Players
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

    check.equal(status_code, status)
    check.equal(json['needactivation'], False)
    check.equal(json['verifytype'],    'none')
    check.equal(json['remaintime'],        -1)
    check.is_not_in(json['token'],         '')
    check.equal(json['settle'],          True)


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

    check.equal(status_code, status)
    check.equal(json['code'], 2)
    check.equal(json['msg'], 'userid or password is incorrect')
    check.equal(json['replace'], None)


@allure.feature('Login')
@allure.story('Minus')
@allure.step('')
def test_login_with_username_unknown_input(usernames=['12345678901234', '叫我第一名', '!@#!*@&^#*'],
                                                  status=wrong_status):
    player = Players(env)
    for username in usernames:
        status_code, json = player.login(username)

        check.equal(status_code, status)
        check.equal(json['code'], 2)
        check.equal(json['msg'], 'userid or password is incorrect')
        check.equal(json['replace'], None)


@allure.feature('Login')
@allure.story('Minus')
@allure.step('')
def test_login_with_null_username(username=None, status=wrong_status):
    player = Players(env)
    status_code, json = player.login(username)

    check.equal(status_code, status)
    check.equal(json['code'], 0)
    check.equal(json['msg'], 'Invalid param: loginname is empty')
    check.equal(json['replace'], None)


@allure.feature('Login')
@allure.story('Minus')
@allure.step('')
def test_login_with_null_pwd(username='welly', pwd=None, status=wrong_status):
    player = Players(env)
    status_code, json = player.login(username, pwd)

    check.equal(status_code, status)
    check.equal(json['code'], 0)
    check.equal(json['msg'], 'Invalid param: loginpassword is empty')
    check.equal(json['replace'], None)


@allure.feature('Login')
@allure.story('Minus')
@allure.step('')
def test_login_with_null_username_and_pwd(username=None, pwd=None, status=wrong_status):
    player = Players(env)
    status_code, json = player.login(username, pwd)

    check.equal(status_code, status)
    check.equal(json['code'], 0)
    check.equal(json['msg'], 'Invalid param: loginname is empty')
    check.equal(json['replace'], None)


@allure.feature('Logout')
@allure.story('Positive')
@allure.step('')
def test_logout_success(status=204):
    player = Players(env)
    status_code = player.logout()

    check.equal(status_code, status)


def lookup_success(usernames, status):
    player = Players(env)

    for username in usernames:
        status_code, jsons = player.lookup(username)

        check.equal(status_code, status)
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
            check.equal(status_code, wrong_status)
            check.equal(json['code'], 0)
            check.equal(json['msg'], 'Invalid param: q should not be smaller than 3')

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

    check.equal(json['playerid'], username)
    check.equal(json['currency'], 'CNY')
    check.equal(json['firstname'], username)
    check.equal(json['birthdate'], 1034352000000)
    check.equal(json['birthday'], 1034352000000)
    check.equal(json['mobile'], '86 13131313131')
    check.equal(json['im1'], None)
    check.equal(json['im2'], None)
    check.equal(json['tagnames'], None)
    check.equal(json['affiliateid'], None)
    check.equal(json['createdate'], 1602475428095,)
    check.not_equal(json['lastlogintime'], 1603431826657)
    check.equal(json['internalplayer'], False)
    check.equal(json['withdrawid'], None)
    check.equal(json['settle'], True)
    check.equal(json['agentid'], None)
    check.equal(json['pic1id'], None)
    check.equal(json['pic2id'], None)
    check.equal(json['pic1'], None)
    check.equal(json['pic2'], None)
    check.equal(json['hasverifiedmobile'], False)
    displayname = json['displayname']
    check.equal(displayname['en-US'], '青銅_English')
    check.equal(displayname['hi-IN'], '青銅_印度語')
    check.equal(displayname['id-ID'], '青銅_ndonesia')
    check.equal(displayname['ja-JP'], '青銅_日本語')
    check.equal(displayname['ml-IN'], None)
    check.equal(displayname['ms-MY'], '青銅_Melayu')
    check.equal(displayname['my-MM'], None)
    check.equal(displayname['ta-IN'], None)
    check.equal(displayname['th-TH'], '青銅_ไทย')
    check.equal(displayname['vi-VN'], '青銅_Tiếng Việt')
    check.equal(displayname['zh-CN'], '青銅_簡體中文')
    check.equal(displayname['zh-TW'], '青銅_james')
    check.equal(json['showforec'], True)
    check.equal(json['ulagentid'], None)
    check.equal(json['ulagentaccount'], None)


@allure.feature('Random')
@allure.story('Positive')
@allure.step('')
def test_random_success(methods=['get', 'post']):
    players = Players(env)

    for method in methods:
        status_code, json = players.random(method)

        check.is_not_none(json['uuid'])
        check.is_not_none(json['image'])


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
    # print(json)
    # with open('rrrr.json', 'r', encoding='utf-8') as f:
    #     for file in f:
    #         file1 = file
    #
    # # with open('trrrrr.json', 'r', encoding='utf-8') as f:
    # #     for file in f:
    # #         file2 = file
    #
    # import json
    # a = json.loads(file1)
    # print(type(a), a)


# Information is too less
def test_register_isplayerinforready(username='welly1'):
    players = Players(env)
    userinfo = UserInfo(username)

    user = userinfo.username()
    pwd = userinfo.pwd()

    status_code, json = players.register_isplayerinforready(user, pwd)
    pprint(json)


if __name__ == '__main__':
    subprocess.call(['pytest', '-vs', 'test_players.py::test_register_isplayerinforready'])
    # os.system('del /q report')
    # pytest.main(['-vs', '--alluredir', 'report'])
    # subprocess.call(['pytest', '-vs', 'test_players.py::test_profile', '--alluredir', 'report'])

