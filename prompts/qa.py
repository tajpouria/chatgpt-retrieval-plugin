from langchain.prompts import PromptTemplate

template = """The following is a friendly conversation between a human and an customer support AI.
The AI identifies itself as: {agentbot_description}.
The AI is talkative and provides lots of specific details from its context.
If the AI does not know the answer to a question, it says it does not know, and ask human to connect to customer support.
The AI will answer in {content_language}.
%%
Context:
{context}
%%
Current conversation:
{history}
Human: {content}
AI: """

prompt = PromptTemplate(
    input_variables=[
        "history",
        "agentbot_description",
        "context",
        "content_language",
        "content",
    ],
    template=template,
)
