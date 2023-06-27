from langchain.llms import OpenAI
from langchain.output_parsers import PydanticOutputParser

from pydantic import BaseModel, Field, validator
from typing import List
llm = OpenAI(temperature=0)
# 出力データ構造の定義
SHIKOKU = ('香川県','愛媛県','徳島県','高知県')

class SouvenirInShikoku(BaseModel):
    name: str = Field(description="県名")
    specialty: List[str] = Field(description="その県の特産品")
parser = PydanticOutputParser(pydantic_object=SouvenirInShikoku)
from langchain.prompts import PromptTemplate
prompt = PromptTemplate(
    template="Answer the user query.\n{format_instructions}\n{query}\n",
    input_variables=["query"],
    partial_variables={"format_instructions": parser.get_format_instructions()}
)
ask_query = "高知の特産品を教えて"

_input = prompt.format_prompt(query=ask_query)
output = llm(_input.to_string())

parser.parse(output)