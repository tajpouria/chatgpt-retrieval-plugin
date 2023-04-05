import os
from chatwoot.services.send_message_to_conversation import (
    send_message_to_conversation,
)
from chatwoot.schemas.common import AccountSettings
from bot.schemas.message_created import ContentType, MessageCreatedEvent
from services.logger import logger
from services.translate import translate_text
from services.query_parser import concatenate_query_results
from dict_deep import deep_get
from datastore.factory import datastore, get_namespace_name
from prompts.qa import prompt as qa_prompt
from models.models import Query
from langchain.memory.chat_message_histories import RedisChatMessageHistory
from langchain.memory import ConversationBufferMemory
from langchain import OpenAI, LLMChain

CHATWOOT_URL = os.getenv("CHATWOOT_URL")
CHATWOOT_BOT_TOKEN = os.getenv("CHATWOOT_BOT_TOKEN")
CHATWOOT_PLATFORM_TOKEN = os.getenv("CHATWOOT_PLATFORM_TOKEN")
CHATWOOT_USER_TOKEN = os.getenv("CHATWOOT_USER_TOKEN")
CHATWOOT_AGENTBOT_OUTGOING_URL = os.getenv("CHATWOOT_AGENTBOT_OUTGOING_URL")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
CONVERSATION_HISTORY_TTL = int(os.getenv("CONVERSATION_HISTORY_TTL", 60 * 60 * 24 * 3))

agentbot_description = "Fly With Bot is an AI-powered chatbot designed to assist customers with information on Fly With Pouria, an online travel business offering ticket selling, car renting, and hotel renting services. Available 24/7, Fly With Bot provides customers with up-to-date and accurate information on Fly With Pouria's products and services, including pricing and availability. Customers can also receive recommendations based on their preferences and previous booking history, and Fly With Bot can even assist with last-minute changes or cancellations. With its natural language processing capabilities and user-friendly interface, Fly With Bot is the perfect travel companion for anyone looking to book travel services with Fly With Pouria."


async def process_message_created_event(
    agentbot_id: int, event_data: MessageCreatedEvent
):
    """Handle a 'message_created' event.

    Args:
        event_data: The event data, represented as a Pydantic model instance.

    Returns:
        None.
    """
    logger.info(
        "Agentbot %s Received a 'message_created' event: %s", agentbot_id, event_data
    )

    message_type = event_data.get("message_type")
    if message_type == "outgoing":
        logger.info("Ignoring outgoing message")
        return

    content_type = ContentType(event_data.get("content_type"))
    if content_type == ContentType.text:
        await handle_text_content(agentbot_id, event_data)
        pass
    else:
        handle_unknown_content_type(event_data)
        pass


async def handle_text_content(
    agentbot_id: int, event_data: MessageCreatedEvent
) -> None:
    """Handle text content.

    Args:
        event_data: The event data, represented as a Pydantic model instance.

    Returns:
        None.
    """

    logger.info(
        "Received a 'message_created' event with text content: %s",
        event_data.get("content"),
    )

    content: str = deep_get(event_data, "content")
    account_id: int = deep_get(event_data, "account.id")
    conversation_id: int = deep_get(event_data, "conversation.id")

    if not content or not account_id or not conversation_id:
        logger.error(
            "Received a 'message_created' event with missing content or account or conversation ID"
        )
        return

    # TODO: Must be calculated dynamically
    settings = AccountSettings(
        chatwoot_url=CHATWOOT_URL,
        chatwoot_bot_token=CHATWOOT_BOT_TOKEN,
        chatwoot_platform_token=CHATWOOT_PLATFORM_TOKEN,
        chatwoot_user_token=CHATWOOT_USER_TOKEN,
        chatwoot_account_id=account_id,
    )

    chat_history = RedisChatMessageHistory(
        session_id=str(conversation_id), url=REDIS_URL, ttl=CONVERSATION_HISTORY_TTL
    )

    # Get the translated query
    # TODO: We must setup a way to get the user's knowledge base language
    try:
        translated_content, content_language = translate_text("en", content)
    except Exception as e:
        logger.error("Error translating text: %s", e)
        # TODO: Extract the bot failure messages to a separate module with translations for each language
        response = send_message_to_conversation(
            conversation_id,
            "Oops, something went wrong. Please try again later.",
            settings=settings,
        )
        if response.status_code != 200:
            logger.error(
                "Send message to conversation failed, response body: %s", response.text
            )

        return

    # Query the Datastore
    try:
        # TODO: Add the common namespace query as well namespace=hoory for example
        datastore_results = await datastore.query(
            queries=[
                Query(
                    query=translated_content,
                    namespace=get_namespace_name(
                        account_id=account_id, agentbot_id=agentbot_id
                    ),
                    top_k=3,
                )
            ]
        )
        query_results = concatenate_query_results(datastore_results)
    except Exception as e:
        logger.error("Error querying the datastore: %s", e)
        response = send_message_to_conversation(
            conversation_id,
            "Oops, something went wrong. Please try again later.",
            settings=settings,
        )
        if response.status_code != 200:
            logger.error(
                "Send message to conversation failed, response body: %s",
                response.text,
            )

        return

    # Get the LLM response
    try:
        memory = ConversationBufferMemory(input_key="content", chat_memory=chat_history)
        chain = LLMChain(
            llm=OpenAI(temperature=0),
            prompt=qa_prompt,
            memory=memory,
            verbose=True,
        )
        ai_content = chain.predict(
            agentbot_description=agentbot_description,
            context=query_results.get("account"),
            content_language=content_language,
            content=content,
        )
    except Exception as e:
        logger.error("Error generating the response: %s", e)
        response = send_message_to_conversation(
            conversation_id,
            "Oops, something went wrong. Please try again later.",
            settings=settings,
        )
        if response.status_code != 200:
            logger.error(
                "Send message to conversation failed, response body: %s",
                response.text,
            )

        return

    response = send_message_to_conversation(
        conversation_id,
        ai_content,
        settings=settings,
    )
    if response.status_code != 200:
        logger.error(
            "Send message to conversation failed, response body: %s", response.text
        )


def handle_unknown_content_type(event_data: MessageCreatedEvent):
    """Handle unknown content types.

    Args:
        event_data: The event data, represented as a Pydantic model instance.

    Returns:
        None.
    """
    logger.warning(
        "Received a 'message_created' event with unknown content type: %s",
        event_data.get("content_type"),
    )
    pass
