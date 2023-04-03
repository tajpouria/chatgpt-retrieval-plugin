import streamlit as st

from chatwoot.services.list_all_agentbots import list_all_agentbots
from chatwoot.services.create_an_agentbot import create_an_agentbot
from chatwoot.services.delete_an_agentbot import delete_an_agentbot
from chatwoot.schemas.common import AccountSettings


# This is will be dynamic in the future.
account_settings = AccountSettings(
    chatwoot_url=st.secrets["CHATWOOT_URL"],
    chatwoot_bot_token=st.secrets["CHATWOOT_BOT_TOKEN"],
    chatwoot_user_token=st.secrets["CHATWOOT_USER_TOKEN"],
    chatwoot_platform_token=st.secrets["CHATWOOT_PLATFORM_TOKEN"],
    chatwoot_account_id=2,
)

st.set_page_config(
    page_title="ChatBots",
    page_icon="🤖",
)

st.title("🤖 ChatBots")


def create_chatbot(name: str, description: str) -> None:
    if not name:
        st.error("Name is required.")
        return
    if not description:
        st.error("Description is required.")
        return

    response = create_an_agentbot(
        name,
        description,
        st.secrets["CHATWOOT_AGENTBOT_OUTGOING_URL"],
        account_settings,
    )
    if response.status_code != 200:
        st.error(f"There was an error while creating the chatbot: {response.text}")
        return

    st.success(f"ChatBot {name} created successfully.")
    st.experimental_rerun()


with st.form("create_chatbot_form"):
    name = st.text_input("Name", placeholder="Name of the ChatBot.")
    description = st.text_area(
        "Description",
        placeholder="What's the purpose of the ChatBot. Chat bot will use this description to identify itself in the conversation.",
    )
    submitted = st.form_submit_button("Create a ChatBot")
    if submitted:
        create_chatbot(name, description)


def delete_chatbot(id: int) -> None:
    # TODO: Delete Awareness and Rulings as well

    response = delete_an_agentbot(id, account_settings)
    if response.status_code != 200:
        st.error(f"There was an error while deleting the agentbot: {response.text}")
        return

    st.success(f"ChatBot {id} deleted successfully.")
    st.experimental_rerun()


def get_agentbots() -> list:
    response = list_all_agentbots(account_settings)
    if response.status_code != 200:
        st.error(f"There was an error while listing the agentbots: {response.text}")
        return []

    return response.json()


agentbots = get_agentbots()

if len(agentbots) == 0:
    st.write("This workspace doesn't have chatbots, yet.")
else:
    cols = st.columns(4)
    cols[0].write("**ID**")
    cols[1].write("**Name**")

    # rows
    for agent in agentbots:
        agent_id = agent["id"]

        col1, col2, col3, col4, col5 = st.columns(5)
        col1.write(str(agent_id))
        col2.write(str(agent["name"]))

        placeholder = col3.empty()
        placeholder.write(
            "[🧠 Awareness](%s)" % "http://localhost:8502?agentbot_id=%s" % agent_id
        )

        placeholder = col4.empty()
        placeholder.write(
            "[🤔 Ruling](%s)" % "http://localhost:8502?agentbot_id=%s" % agent_id
        )

        placeholder = col5.empty()
        delete = placeholder.button("Delete", key=agent_id)
        if delete:
            delete_chatbot(agent_id)
