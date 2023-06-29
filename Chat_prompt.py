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

Json_template="""
{
    "@context":"https://schema.org/"
    "@type":"Clip"
    "name":
    "description":
    "keywords":[]
    "contentLocation":[
    {
        "@type":Place
        "name":
        "sameAs":
        "address":{
            "@type":"PostalAddress",
            "addressCountry":
            "adsressRegion":
        }
    },
    
    ]

}
"""


words_list="根室本線、北海道、滝川駅、帯広、釧路、根室駅、花咲線、リゾート列車、キハ283系、丹頂鶴、北海道らしさ"
entity_list="""{
    {"北海道-都道府県-北海道": "https://ja.wikipedia.org/wiki/北海道"},
    {"滝川駅-駅-滝川駅": "https://ja.wikipedia.org/wiki/滝川駅"},
    {"帯広市-市-帯広市": "https://ja.wikipedia.org/wiki/帯広市"},
    {"釧路市-市-釧路市": "https://ja.wikipedia.org/wiki/釧路市"},
    {"根室駅-駅-根室駅": "https://ja.wikipedia.org/wiki/根室駅"},
    {"花咲線-路線-花咲線": "https://ja.wikipedia.org/wiki/花咲線"},
    {"キハ283系-車両-キハ283系": "https://ja.wikipedia.org/wiki/キハ283系"},
    {"丹頂鶴-鳥類-丹頂鶴": "https://ja.wikipedia.org/wiki/丹頂鶴"}
}
"""
chat =ChatOpenAI(temperature=0)
messages = [
    HumanMessage(content=f"{entity_list}の中から都道府県名、市区町村名、駅名を表す要素のみ抜き出して、wikipediaのリンクと合わせて出力してください")
]
result = chat(messages)
entity_list = result.content
messages=[
    HumanMessage(content=f"""説明文とピックアップしたキーワード {words_list}と都道府県・市区町村・駅名{entity_list}を使ってSchema.org の Clip クラスを用いて生成して。
ただし、{Json_template}を埋めるようにエンコードすること。
""")
]
result=chat(messages)
print(result.content)
