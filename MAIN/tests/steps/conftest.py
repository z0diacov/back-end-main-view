import sys
import os
sys.path.insert(0, os.path.dirname(__file__).replace('\\', '/') + '/../../')

from pytest import fixture
from fastapi.testclient import TestClient
from main import app
from tests.database_for_tests import mysql_client_sync
from tests.database_for_tests import redis_client_sync

@fixture(scope="session")
def client() -> TestClient:
    with TestClient(app) as test_client:
        yield test_client


@fixture(scope="module", autouse=True)
def prepare_database():
    try:
        mysql_client_sync.connect()
        redis_client_sync.connect()
        mysql_client_sync.refresh_db()
        redis_client_sync.clear()
        yield
    except Exception as e:
        print(f"Error: {e}")
    finally:
        mysql_client_sync.disconnect()
        redis_client_sync.disconnect()

@fixture
def data() -> dict[str, str | int | bool]:
    return {}


@fixture
def response_fixture() -> dict:
    return {}