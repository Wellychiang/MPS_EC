import pytest
import pytest_check as check
import os
import allure
from base_api.base_players import Players

env = 'stg'
status = 200
wrong_status = 498


def test_login_success(username='welly'):
    player = Players(env)
    status_code, json = player.login(username)

    check.equal(status_code, 498)
    check.equal(json['needactivation'], False)
    check.equal(json['verifytype'],    'none')
    check.equal(json['remaintime'],        -1)
    check.is_not_in(json['token'],         '')
    check.equal(json['settle'],          True)


def test_login_wrong_pwd(username='welly', pwd='asodijaosia'):
    player = Players(env)
    player.login(username, pwd)
    status_code, json = player.login(username, pwd)

    check.equal(status_code, wrong_status)
    check.equal(json['code'], 2)
    check.equal(json['msg'], 'userid or password is incorrect')
    check.equal(json['replace'], None)


def test_login_null_username(username=''):
    player = Players(env)
    player.login(username)
    status_code, json = player.login(username)

    check.equal(status_code, wrong_status)
    check.equal(json['code'], 0)
    check.equal(json['msg'], 'Invalid param: loginname is empty')
    check.equal(json['replace'], None)


def test_login_null_pwd(username='welly', pwd=''):
    player = Players(env)
    player.login(username)
    status_code, json = player.login(username, pwd)

    check.equal(status_code, wrong_status)
    check.equal(json['code'], 0)
    check.equal(json['msg'], 'Invalid param: loginname is empty')
    check.equal(json['replace'], None)


if __name__ == '__main__':
    pytest.main(['-vs'])
    # os.system('del /q report')
    # pytest.main(['-vs', '--alluredir', 'report'])
    # os.system('allure generate report --clean')
    # os.system('allure open')
