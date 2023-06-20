from langchain.chat_models import ChatOpenAI
# チャットモデルで利用可能なメッセージの型をインポート
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage,
)
sample_word=input()
word_list=["東京駅","さいたま市","神奈川駅"]
example_list=[]
# チャットモデルのラッパーを初期化
chat = ChatOpenAI(temperature=0)
# チャットモデルにメッセージを渡して、予測を受け取る
# チャットモデルに渡すメッセージを作成する
for word in word_list:
    messages1 = [
    SystemMessage(content="あなたは与えられた単語に関してShcema.orgのJSON-LDを用いて記述するエージェントです。この時schema:location を使ってエンコードしてください"),
    HumanMessage(content=word)
    ]

    result=chat(messages1)
    print(result.content)
    example_list.append({"location":sample_word,"JSON-LD":result.content})
    print(example_list)