from pydantic import BaseSettings


class AccountSettings(BaseSettings):
    chatwoot_url: str
    chatwoot_bot_token: str
    chatwoot_platform_token: str
    chatwoot_user_token: str
    chatwoot_account_id: int