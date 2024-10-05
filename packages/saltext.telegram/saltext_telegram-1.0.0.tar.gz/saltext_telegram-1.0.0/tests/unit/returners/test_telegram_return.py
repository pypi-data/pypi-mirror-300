"""
    Test Telegram Returner

    :codeauthor: :email:`Roald Nefs (info@roaldnefs.com)`
"""

from unittest.mock import MagicMock
from unittest.mock import patch

import pytest

import saltext.telegram.returners.telegram_return as telegram


@pytest.fixture
def configure_loader_modules():
    return {telegram: {}}


def test_returner():
    """
    Test to see if the Telegram returner sends a message
    """
    ret = {
        "id": "12345",
        "fun": "mytest.func",
        "fun_args": "myfunc args",
        "jid": "54321",
        "return": "The room is on fire as shes fixing her hair",
    }
    options = {"chat_id": "", "token": ""}

    with patch(
        "saltext.telegram.returners.telegram_return._get_options",
        MagicMock(return_value=options),
    ), patch.dict(
        "saltext.telegram.returners.telegram_return.__salt__",
        {"telegram.post_message": MagicMock(return_value=True)},
    ):
        assert telegram.returner(ret) is True
