from langchain.chat_models import ChatOpenAI
from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
import json
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage,
    LLMResult,
)
from langchain.chains import ConversationChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
chat = ChatOpenAI(temperature=0)
prompt = ChatPromptTemplate.from_messages(
    [
        MessagesPlaceholder(variable_name="history"),
        SystemMessagePromptTemplate.from_template(
            """あなたは入力された要素に対して,schema.orgでその要素を記述するのに適切なクラスやプロパティを出力するエージェントです
"""
        ),
        HumanMessagePromptTemplate.from_template("{input}"),

    ]
)
memory = ConversationBufferMemory(return_messages=True, memory_key="history")
conversation = ConversationChain(memory=memory, prompt=prompt, llm=chat, verbose=True)

a1 = conversation.run(input="都道府県")
print(a1)
a2 = conversation.run(input="市町村名")
print(a2)
a3 = conversation.run(input = "駅名")
print(a3)