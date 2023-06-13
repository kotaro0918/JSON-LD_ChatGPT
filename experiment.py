from langchain.chat_models import ChatOpenAI
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
result_list = []
# チャットモデルで利用可能なメッセージの型をインポート
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage,
    LLMResult,
)

# チャットモデルのラッパーを初期化
chat = ChatOpenAI(temperature=0)

# チャットモデルに渡すメッセージを作成する
batch_messages = [
    [
        SystemMessage(content="あなたは与えられた文章の中から都道府県名、市区町村名、駅名を表す単語を抜き出して\
         関連したwikipediaの情報と併せてJSON形式で出力するエージェントです。なかった場合はnullを返してください."),
        HumanMessage(content=sample_text),
        AIMessage(content=sample_result),
        HumanMessage(content=target_text),
    ],
    [
        SystemMessage(content="あなたは与えられた文章の中からキーワードとタイトルを抜き出してJSON形式で出力するエージェントです"),
        HumanMessage(content=target_text),
    ],
]

# チャットモデルにメッセージを渡して、予測を受け取る
result: LLMResult = chat.generate(batch_messages)
result_list=result.generations
chat = ChatOpenAI(temperature=0)

messages = [
    SystemMessage(content="動画の紹介文とそれから抜き出したデータを使いschema.orgのClipクラスを用いてJSON-LD形式で記述してください.\
         typeがThingなものは除外してください"),
    HumanMessage(content=result_list)
]

# チャットモデルにメッセージを渡して、予測を受け取る
result = chat(messages)
print(result.content)



