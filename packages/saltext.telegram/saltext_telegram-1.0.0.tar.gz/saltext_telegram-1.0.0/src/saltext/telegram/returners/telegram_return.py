"""
Return Salt data via Telegram.

To use the Telegram returner, append ``--return telegram`` to the Salt command.

.. code-block:: bash

    salt '*' test.ping --return telegram
"""

import logging

import salt.returners

log = logging.getLogger(__name__)

__virtualname__ = "telegram"


def _get_options(ret=None):
    """
    Get the Telegram options from salt.

    :param ret:     The data to be sent.
    :return:        Dictionary containing the data and options needed to send
                    a message to Telegram.
    """
    attrs = {"chat_id": "chat_id", "token": "token"}

    _options = salt.returners.get_returner_options(
        __virtualname__, ret, attrs, __salt__=__salt__, __opts__=__opts__
    )
    log.debug("Options: %s", _options)
    return _options


def returner(ret):
    """
    Send a Telegram message with the data.

    :param ret:     The data to be sent.
    :return:        Boolean if message was sent successfully.
    """
    _options = _get_options(ret)

    chat_id = _options.get("chat_id")
    token = _options.get("token")

    if not chat_id:
        log.error("telegram.chat_id not defined in salt config")
    if not token:
        log.error("telegram.token not defined in salt config")

    returns = ret.get("return")

    message = "id: {}\r\nfunction: {}\r\nfunction args: {}\r\njid: {}\r\nreturn: {}\r\n".format(
        ret.get("id"), ret.get("fun"), ret.get("fun_args"), ret.get("jid"), returns
    )

    return __salt__["telegram.post_message"](message, chat_id=chat_id, token=token)
