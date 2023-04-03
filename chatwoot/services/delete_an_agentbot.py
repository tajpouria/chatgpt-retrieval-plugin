from typing import Dict, Any
import requests

from chatwoot.schemas.common import AccountSettings


def delete_an_agentbot(id: str, settings: AccountSettings) -> Dict[str, Any]:
    """
    Deletes an agentbot.

    Args:
        id (str): The ID of the agentbot to delete.
        settings (AccountSettings): The settings for the account.

    Returns:
        Dict[str, Any]: A dictionary containing the response from the Chatwoot API.
    """
    url = f"{settings.chatwoot_url}/api/v1/accounts/{settings.chatwoot_account_id}/agent_bots/{id}"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "api_access_token": f"{settings.chatwoot_user_token}",
    }

    return requests.delete(url, headers=headers)
