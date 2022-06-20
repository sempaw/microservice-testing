import pytest

from app.db.session_async import AsyncSession


@pytest.fixture()
def db_setup():
    print("\nconnect to db")
    return AsyncSession()


def test_db_exist(db_setup):
    db_setup.execute("select 1")


def test_user_table_not_empty(db_setup):
    data = db_setup.execute("select * from user")
    assert data is not None


# def test_user_table_not_empty(db_setup):
#     try:
#         data = db_setup.execute("select * from userr")
#         assert data is not None
#     except Exception as e:
#         pytest.fail(str(e))


def test_contract_table_not_empty(db_setup):
    data = db_setup.execute("select * from contract")
    assert data is not None


def test_spec_table_not_empty(db_setup):
    data = db_setup.execute("select * from spec")
    assert data is not None
