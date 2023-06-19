from langchain.chat_models import ChatOpenAI
from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.chains import ConversationChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory


chat = ChatOpenAI(temperature=0)

target_text= "根室本線は北海道の滝川駅から帯広、釧路を経て根室駅を結ぶＪＲ北海道の路線です。このうち釧路駅から\
    根室駅までの区間は「花咲線」の愛称で呼ばれています。観光シーズンには札幌からのリゾート列車が多数運行されます。キハ283系の車体は、\
    ブルーとグリーンに丹頂鶴の赤を組み合わせ北海道らしさを演出しています."
sample_text = "三郷市は、埼玉県南東部にあり、東京都と千葉県に接しています。名物の小松菜はハウス栽培で１年を通して出荷されます。\
         小松菜を使った新しい料理にも取り組んでいます。「小松菜餃子」は、小松菜パウダーを皮に練りこみ、具にも小松菜がたっぷりと入っています。"
sample_result='''
{
    {"三郷市-市-三郷市": "https://ja.wikipedia.org/wiki/三郷市"},
    {"埼玉県-都道府県-埼玉県": "https://ja.wikipedia.org/wiki/埼玉県"},
    {"東京都-都道府県-東京都": "https://ja.wikipedia.org/wiki/東京都"},
    {"千葉県-都道府県-千葉県": "https://ja.wikipedia.org/wiki/千葉県"},
}
'''

prompt = ChatPromptTemplate.from_messages(
    [
        MessagesPlaceholder(variable_name="history"),
        SystemMessagePromptTemplate.from_template(
            """あなたは以下の動画に関する説明文についての質問に回答するエージェントです。

text:根室本線は北海道の滝川駅から帯広、釧路を経て根室駅を結ぶＪＲ北海道の路線です。
このうち釧路駅から根室駅までの区間は「花咲線」の愛称で呼ばれています。
観光シーズンには札幌からのリゾート列車が多数運行されます。
キハ283系の車体は、ブルーとグリーンに丹頂鶴の赤を組み合わせ北海道らしさを演出しています.

"""
        ),
        HumanMessagePromptTemplate.from_template("{input}"),
    ]
)
prompt2=ChatPromptTemplate.from_messages(
    [       
        SystemMessagePromptTemplate.from_template(
            """あなたは以下の動画に関する説明文についての質問に回答するエージェントです。

text:根室本線は北海道の滝川駅から帯広、釧路を経て根室駅を結ぶＪＲ北海道の路線です。
このうち釧路駅から根室駅までの区間は「花咲線」の愛称で呼ばれています。
観光シーズンには札幌からのリゾート列車が多数運行されます。
キハ283系の車体は、ブルーとグリーンに丹頂鶴の赤を組み合わせ北海道らしさを演出しています.

"""
        ),
        MessagesPlaceholder(variable_name="history"),
        HumanMessagePromptTemplate.from_template("{input}"),
    ]

)
memory = ConversationBufferMemory(return_messages=True, memory_key="history")
conversation = ConversationChain(memory=memory, prompt=prompt, llm=chat, verbose=True)
memory.chat_memory.add_user_message(f"あなたは以下のテキスト{sample_text}から市町村名を抜き出して出力するエージェントです")
memory.chat_memory.add_ai_message(f"{sample_result}")

words_list = conversation.run(input="キーワードとタイトルをピックアップして")

print(words_list)

entity_list = conversation.run("例のように都道府県・市区町村・駅名をピックアップした後、関連したwikipdiaのリンクを表示してください")

print(entity_list)

target_JSON = conversation.run(
    input=f"""説明文とピックアップしたキーワード {words_list}と都道府県・市区町村・駅名{entity_list}を使ってSchema.org の Clip クラスを用いて JSON-LD を生成して。
ただし、キーワードは schema:keywords, タイトルは schema:name, 都道府県・市区町村は schema:location を使ってエンコードすること。
"""
)

print(target_JSON)