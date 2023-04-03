from typing import Dict, Any
import requests

from chatwoot.schemas.common import AccountSettings


def create_an_agentbot(
    name: str, description: str, outgoing_url: str, settings: AccountSettings
) -> Dict[str, Any]:
    """
    Creates a new agentbot.

    Args:
        name (str): The name of the agentbot.
        description (str): The description of the agentbot.
        outgoing_url (str): The outgoing URL of the agentbot. This is the URL that agentbot will receive the event from.
        settings (AccountSettings): The settings for the account.

    Returns:
        Dict[str, Any]: A dictionary containing the response from the Chatwoot API.
    """
    url = f"{settings.chatwoot_url}/api/v1/accounts/{settings.chatwoot_account_id}/agent_bots"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "api_access_token": f"{settings.chatwoot_user_token}",
    }
    data = {"name": name, "description": description, "outgoing_url": outgoing_url}

    return requests.post(url, headers=headers, json=data)
