from langchain.llms import OpenAI

# TODO: UserWarning: You are trying to use a chat model. This way of initializing it is no longer supported.
# Instead, please use: `from langchain.chat_models import ChatOpenAI`
llm = OpenAI(model_name="gpt-3.5-turbo-0301")
