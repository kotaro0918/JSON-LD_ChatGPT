from langchain.output_parsers import PydanticOutputParser
from typing import List
from langchain import
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
model_name = "text-davinci-003"
# model = OpenAI(model_name="text-ada-001", n=2, best_of=2)
temperature = 0.0
model = OpenAI(model_name=model_name, temperature=temperature)
from typing import List

from pydantic import BaseModel, Field


class LocationItem(BaseModel):
    _type: str = Field(..., alias='@type',description="どの型に単語が属するか")
    name: str 
    url: str


class Model(BaseModel):
    _context: str = Field(..., alias='@context',description="Schema.org")
    _type: str = Field(..., alias='t@ype')
    name: str
    description: str
    keywords: List[str]
    location: List[LocationItem]
from typing import List,Dict
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



# 言語モデルにデータ構造を埋めるように促す Query
JSON_query =f"""説明文とピックアップしたキーワード {words_list}と都道府県・市区町村・駅名{entity_list}を使ってSchema.org の Clip クラスを用いてJSONで生成して。
ただし、キーワードは schema:keywords, タイトルは schema:name, 都道府県・市区町村・駅名は schema:location を使ってエンコードすること。
"""

# Parser に元になるデータの型を提供する
parser =  PydanticOutputParser(pydantic_object=Model)

# input_variables ではなく、 partial_variables に parser からオブジェクトの説明を入力する
prompt = PromptTemplate(
    template="Answer the user query and answer should be formatted in JSON. \n{format_instructions}\n{query}\n",
    input_variables=["query"],
    partial_variables={"format_instructions": parser.get_format_instructions()}
)
_input = prompt.format_prompt(query=JSON_query)

output = model(_input.to_string())
print(parser.parse(output))
print(parser.get_format_instructions())