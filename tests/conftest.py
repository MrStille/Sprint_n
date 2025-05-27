import pytest

from Data import Data
from helpers.AdHelper import AdHelper
from helpers.RandomHelpers import RandomHelpers
from steps.steps import Steps


@pytest.fixture(scope='function')
def new_user():
    return RandomHelpers.get_random_user()

@pytest.fixture(scope='function')
def registered_user(new_user):
    register_response = Steps.register_new_user(new_user)
    assert register_response.status_code == 201
    return {
        "email": new_user["email"],
        "password": new_user["password"],
        "access_token": register_response.json()["access_token"]["access_token"]
    }

@pytest.fixture(scope='function')
def logged_user(registered_user):
    register_response = Steps.login_user(registered_user)
    assert register_response.status_code == 201
    return {
        "email": registered_user["email"],
        "password": registered_user["password"],
        "access_token": register_response.json()["token"]["access_token"]
    }

@pytest.fixture(scope='function')
def created_ads(logged_user):
    expected_ads = AdHelper.get_random_ads()
    created_ads = Steps.create_ads_ok(logged_user, expected_ads)
    yield created_ads
    Steps.delete_ads(logged_user, created_ads)