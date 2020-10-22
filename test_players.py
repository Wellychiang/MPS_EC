import pytest
import pytest_check as check
import os
import allure
from base_api.base_players import Players
from config.user import UserInfo


env = 'stg'
right_status = 200
wrong_status = 498


def base_login_success(user='welly'):
    player = Players(env)
    user_info = UserInfo(user)
    username = user_info.username()
    pwd = user_info.pwd()

    status_code, json = player.login(username, pwd)

    check.equal(status_code, right_status)
    check.equal(json['needactivation'], False)
    check.equal(json['verifytype'],    'none')
    check.equal(json['remaintime'],        -1)
    check.is_not_in(json['token'],         '')
    check.equal(json['settle'],          True)


@allure.feature('Positive')
def test_login_success():
    names = ['welly', 'welly1', 'welly2']
    [base_login_success(name) for name in names]


@allure.feature('Minus')
def test_login_wrong_pwd(username='welly', pwd='asodijaosia'):
    player = Players(env)
    status_code, json = player.login(username, pwd)

    check.equal(status_code, wrong_status)
    check.equal(json['code'], 2)
    check.equal(json['msg'], 'userid or password is incorrect')
    check.equal(json['replace'], None)


@allure.feature('Minus')
def test_login_null_username(username=''):
    player = Players(env)
    status_code, json = player.login(username)

    check.equal(status_code, wrong_status)
    check.equal(json['code'], 0)
    check.equal(json['msg'], 'Invalid param: loginname is empty')
    check.equal(json['replace'], None)


@allure.feature('Minus')
def test_login_null_pwd(username='welly', pwd=''):
    player = Players(env)
    status_code, json = player.login(username, pwd)

    check.equal(status_code, wrong_status)
    check.equal(json['code'], 0)
    check.equal(json['msg'], 'Invalid param: loginpassword is empty')
    check.equal(json['replace'], None)


@allure.feature('Minus')
def test_login_null_username_and_pwd(username='', pwd=''):
    player = Players(env)
    status_code, json = player.login(username, pwd)

    check.equal(status_code, wrong_status)
    check.equal(json['code'], 0)
    check.equal(json['msg'], 'Invalid param: loginname is empty')
    check.equal(json['replace'], None)


if __name__ == '__main__':

    pytest.main(['-vs'])
    os.system('del /q report')
    pytest.main(['-vs', '--alluredir', 'report'])
