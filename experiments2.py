# llm ラッパーのインポート
from langchain import OpenAI
# プロンプトテンプレートのインポート
from langchain.prompts import PromptTemplate

# LLMChain に加えて SimpleSequentialChain もインポートする
# SimpleSequentialChain は、複数のチェーンを連続実行するためのチェーンで以下の特徴をもつ
# - 各ステップの入出力は一つ
# - 各ステップの出力が次のステップの入力になる
from langchain.chains import LLMChain, SimpleSequentialChain
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

# llm ラッパーの初期化
llm = OpenAI(temperature=0)

# 最初のプロンプトテンプレートの作成
prompt_first = PromptTemplate(
    input_variables=["text"],
    template="あなたは与えられた{text}の中から都道府県名、市区町村名、駅名を表す単語とキーワードとタイトルを抜き出して\
         関連したwikipediaの情報と併せてJSON形式で出力するエージェントです。なかった場合はnullを返してください.",
)

# 最初に実行する LLM チェーンを定義
# 会社名を考えてもらう
chain_first = LLMChain(llm=llm, prompt=prompt_first)

# 次のプロンプトテンプレートの作成
prompt_second = PromptTemplate(
    input_variables=["JSON_list"],
    template="動画の紹介文とそれから抜き出したデータ{JSON_list}を使いschema.orgのClipクラスを用いてJSON-LD形式で記述してください.",
)

# 次に実行する LLM チェーンを定義
# キャッチコピーを考えてもらう
chain_second = LLMChain(llm=llm, prompt=prompt_second)

# 二つの LLM チェーンを連結
overall_chain = SimpleSequentialChain(chains=[chain_first, chain_second], verbose=True)

# 連結してできたチェーンを実行
chatchphrase = prediction = overall_chain.run(target_text)
print(chatchphrase)