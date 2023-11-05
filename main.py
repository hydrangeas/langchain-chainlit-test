import chainlit as cl
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.schema import HumanMessage
from langchain.vectorstores import Chroma
from dotenv import load_dotenv
load_dotenv()

embeddings = OpenAIEmbeddings(
    model="text-embedding-ada-002",
)

chat = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0,
    streaming=True,
)

prompt= PromptTemplate(template="""文章を元に質問に答えてください。
文章から回答できない場合は「質問の文脈が不明確なため、正確な回答はできません。」と回答してください。

文章:
{document}

質問: {query}
""", input_variables=["document", "query"])

@cl.on_chat_start
async def on_chat_start():
    await cl.Message(
        content="いつもご利用ありがとうございます。",
        disable_human_feedback=True,
    ).send()

@cl.on_message
async def on_message(input_message: cl.Message):
    print('on_message: ' + input_message.content)

    database = Chroma(
        persist_directory="./.data/",
        embedding_function=embeddings,
    )
    documents = database.similarity_search(input_message.content)

    documents_string = ""
    for document in documents:
        documents_string += f"""
    ---------------------------
    {document.page_content}
    """

    result = chat([
        HumanMessage(content=prompt.format(document=documents_string, query=input_message.content))
    ])
    await cl.Message(content=result.content).send()
