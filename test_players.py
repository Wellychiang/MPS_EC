import pytest
import pytest_check as check
import os
import allure
from base_api.base_players import Players
from config.user import UserInfo


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
def test_login_success_with_three_user(names = ['welly', 'welly1', 'welly2'], status=right_status):

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
def test_login_with_username_input_fourteen_words(username='12345678901234', status=wrong_status):
    player = Players(env)
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
@allure.story('Positive')
@allure.step('')
def test_lookup_wtih_nonexistent(username='asdz11', status=right_status):
    players = Players(env)
    status_code, json = players.lookup(username)

    print(status_code, json)
    check.equal(status_code, status)
    # check.is_in(json, None)


if __name__ == '__main__':
    pytest.main(['-vs', 'test_players.py::test_lookup_wtih_nonexistent'])
    # os.system('del /q report')
    # pytest.main(['-vs', 'test_players.py::test_lookup_success', '--alluredir', 'report'])
    # pytest.main(['-vs', '--alluredir', 'report'])
