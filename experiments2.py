# チャットモデルのラッパーをインポート
from langchain.chat_models import ChatOpenAI
# チャットプロンプト用のテンプレートをインポート
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    AIMessagePromptTemplate,
)

# チャットモデルのラッパーを初期化
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

# SystemMessage 用のテンプレートの作成
template="あなたは与えられた文章の中から都道府県名、市区町村名、駅名を表す単語を抜き出して\
         関連したwikipediaの情報と併せてJSON形式で出力するエージェントです。なかった場合はnullを返してください."
system_message_prompt = SystemMessagePromptTemplate.from_template(template)

# HumanMessage 用のテンプレートの作成
human_template="{sample}"
human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

human_templete2="{target}"
human_message_prompt2 = HumanMessagePromptTemplate.from_template(human_templete2)

ai_templete="{result_sample}"
ai_message_prompt = AIMessagePromptTemplate.from_template(ai_templete)
# Message のテンプレートを組合わせて会話の流れを決めます
messages_template = [
    system_message_prompt,
    human_message_prompt,
    ai_message_prompt,
    human_message_prompt2
]
# チャットプロンプト用のテンプレートを作成します
chat_prompt_template = ChatPromptTemplate.from_messages(messages_template)

# テンプレートに具体値を組み込んでチャットプロンプトを作成します
chat_prompt = chat_prompt_template.format_prompt(sample=sample_text,result_sample=sample_result,target=target_text).to_messages()

# チャットの補完を作成
completion = chat(chat_prompt)
print(completion.content)