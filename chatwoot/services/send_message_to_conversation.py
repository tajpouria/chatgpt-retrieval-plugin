from typing import Dict, Any
import requests

from chatwoot.schemas.common import AccountSettings


def send_message_to_conversation(
    account_id: str,
    conversation_id: str,
    message: str,
    settings: AccountSettings,
) -> Dict[str, Any]:
    """
    Sends a message to a Chatwoot conversation.

    Args:
        account_id (str): The account ID for Chatwoot.
        conversation_id (str): The conversation ID for the conversation to send the message to.
        message (str): The message to send.
        settings (AccountSettings): The settings for the application.

    Returns:
        Dict[str, Any]: A dictionary containing the response from the Chatwoot API.
    """
    data = {"content": message}
    url = f"{settings.chatwoot_url}/api/v1/accounts/{account_id}/conversations/{conversation_id}/messages"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "api_access_token": f"{settings.chatwoot_bot_token}",
    }

    return requests.post(url, json=data, headers=headers)
