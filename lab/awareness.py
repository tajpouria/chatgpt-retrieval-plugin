import streamlit as st
from chatwoot.schemas.common import AccountSettings
from chatwoot.services.get_an_agent_bot_details import get_an_agentbot_details


account_settings = AccountSettings(
    chatwoot_url=st.secrets["CHATWOOT_URL"],
    chatwoot_bot_token=st.secrets["CHATWOOT_BOT_TOKEN"],
    chatwoot_user_token=st.secrets["CHATWOOT_USER_TOKEN"],
    chatwoot_platform_token=st.secrets["CHATWOOT_PLATFORM_TOKEN"],
    chatwoot_account_id=2,
)


query_params = st.experimental_get_query_params()

agentbot_id = query_params.get("agentbot_id", [None])[0]

if not agentbot_id:
    st.error("No agentbot_id query parameter not found!")
    st.stop()

st.set_page_config(
    page_title="Awareness",
    page_icon="🧠",
)
st.title("🧠 Awareness")

response = get_an_agentbot_details(agentbot_id, account_settings)
if response.status_code != 200:
    st.error(f"There was an error while getting the agentbot: {response.text}")
    st.stop()

agentbot = response.json()

with st.sidebar:
    st.title(agentbot["name"])
    st.subheader("Description")
    st.write(agentbot["description"])
    st.subheader("Outgoing URL")
    st.write(agentbot["outgoing_url"])
    st.subheader("Bot Type")
    st.write(agentbot["bot_type"])
    st.subheader("Access Token")
    st.markdown("`%s`" % agentbot["access_token"])
    st.subheader("Bot Config")
    st.write(agentbot["bot_config"])


tab1, tab2 = st.tabs(["📄 Documents", "🎧 Audios"])


with tab1:
    uploaded_file = st.file_uploader(
        "Choose a file to upload",
        type=["txt", "pdf", "docx"],
        help="The file will be uploaded to the server and then sent to the agentbot.",
    )
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
with tab2:
    st.write("Audio")
