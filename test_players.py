import pytest
import pytest_check as check
import os
import allure
from base_api.base_players import Players
from config.user import UserInfo
from pprint import pprint


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


@allure.feature('lookup')
@allure.story('Positive')
@allure.step('')
def test_lookup_success(usernames=['welly', 'wade', 'lily'], status=right_status):
    lookup_success(usernames, status)


@allure.feature('lookup')
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


# @allure.feature('lookup')
# @allure.story('Minus')
# @allure.step('')
# def test_profile(username='welly'):
#     players = Players(env)
#     userinfo = UserInfo(username)
#
#     user = userinfo.username()
#     pwd = userinfo.pwd()
#
#     status_code, json = players.profile(user, pwd)
#     pprint(f'status_code: {status_code}\njson: {json}')


def test_random(method='get'):
    players = Players(env)
    status_code, json = players.random(method)
    print(f'\nstatus_code: {status_code}\n json: {json}')


if __name__ == '__main__':
    pytest.main(['-vs', 'test_players.py::test_random'])
    # os.system('del /q report')
    # pytest.main(['-vs', '--alluredir', 'report'])
    # pytest.main(['-vs', 'test_players.py::test_lookup_success', '--alluredir', 'report'])

