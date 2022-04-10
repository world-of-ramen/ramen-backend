from datetime import timedelta

import jwt
import pytest

from app.models.domain.users import User
from app.services.jwt import ALGORITHM
from app.services.jwt import create_access_token_for_user
from app.services.jwt import create_jwt_token
from app.services.jwt import get_user_id_from_token


def test_creating_jwt_token() -> None:
    token = create_jwt_token(
        jwt_content={"content": "payload"},
        secret_key="secret",
        expires_delta=timedelta(minutes=1),
    )
    parsed_payload = jwt.decode(token, "secret", algorithms=[ALGORITHM])

    assert parsed_payload["content"] == "payload"


def test_creating_token_for_user(test_user: User) -> None:
    token = create_access_token_for_user(user=test_user, secret_key="secret")
    parsed_payload = jwt.decode(token, "secret", algorithms=[ALGORITHM])

    assert parsed_payload["wallet_address"] == test_user.wallet_address


def test_retrieving_token_from_user(test_user: User) -> None:
    token = create_access_token_for_user(user=test_user, secret_key="secret")
    wallet_address = get_user_id_from_token(token, "secret")
    assert wallet_address == test_user.wallet_address


def test_error_when_wrong_token() -> None:
    with pytest.raises(ValueError):
        get_user_id_from_token("asdf", "asdf")


def test_error_when_wrong_token_shape() -> None:
    token = create_jwt_token(
        jwt_content={"content": "payload"},
        secret_key="secret",
        expires_delta=timedelta(minutes=1),
    )
    with pytest.raises(ValueError):
        get_user_id_from_token(token, "secret")
