from langchain import PromptTemplate
from langchain import FewShotPromptTemplate
from langchain.llms import OpenAI

examples =[{'location': '東京', 'JSON': '以下は東京駅のJSON-LD記述例です。\n\n```json\n{\n  "@context": "https://schema.org",\n  "@type": "Place",\n  "name": "東京駅",\n  "address": {\n    "@type": "PostalAddress",\n    "addressLocality": "千代田区",\n    "addressRegion": "東京都",\n    "postalCode": "100-0005",\n    "streetAddress": "丸の内一丁目9-1"\n  },\n  "geo": {\n    "@type": "GeoCoordinates",\n    "latitude": 35.681236,\n    "longitude": 139.767125\n  },\n  "openingHoursSpecification": [\n    {\n      "@type": "OpeningHoursSpecification",\n      "dayOfWeek": [\n        "Monday",\n        "Tuesday",\n        "Wednesday",\n        "Thursday",\n        "Friday"\n      ],\n      "opens": "05:00",\n      "closes": "01:00"\n    },\n    {\n      "@type": "OpeningHoursSpecification",\n      "dayOfWeek": [\n        "Saturday",\n        "Sunday"\n      ],\n      "opens": "05:00",\n      "closes": "24:00"\n    }\n  ],\n  "telephone": "+81-3-3210-0200",\n  "url": "https://www.tokyostationcity.com/"\n}\n```\n\nこの例では、`@type`に`Place`を指定し、`name`には"東京駅"を指定しています。また、`address`には`PostalAddress`を指定し、住所情報を記述しています。`geo`には緯度経度情報を指定し、`openingHoursSpecification`には営業時間を指定しています。`telephone`には電話番号を、`url`には公式ウェブサイトのURLを指定しています。'}, {'location': '東京', 'JSON': '以下は「さいたま市」に関するJSON-LDの例です。\n\n```json\n{\n  "@context": "https://schema.org/",\n  "@type": "City",\n  "name": "さいたま市",\n  "location": {\n    "@type": "Place",\n    "address": {\n      "@type": "PostalAddress",\n      "addressLocality": "さいたま市"\n    }\n  }\n}\n```\n\nこの例では、`@type`プロパティに`City`を指定し、`name`プロパティに「さいたま市」を指定しています。また、`location`プロパティには、`Place`を指定し、`address`プロパティに`PostalAddress`を指定しています。`addressLocality`プロパティにも「さいたま市」を指定しています。これにより、`location`プロパティが`PostalAddress`であることと、`addressLocality`プロパティが「さいたま市」であることが示されます。'}, {'location': '東京', 'JSON': '以下は神奈川駅のJSON-LD記述例です。\n\n```json\n{\n  "@context": "https://schema.org",\n  "@type": "Place",\n  "name": "神奈川駅",\n  "address": {\n    "@type": "PostalAddress",\n    "addressLocality": "神奈川市",\n    "addressRegion": "神奈川県",\n    "postalCode": "221-0056",\n    "streetAddress": "神奈川区鶴屋町1-1"\n  },\n  "geo": {\n    "@type": "GeoCoordinates",\n    "latitude": 35.4714,\n    "longitude": 139.6242\n  },\n  "openingHoursSpecification": [\n    {\n      "@type": "OpeningHoursSpecification",\n      "dayOfWeek": [\n        "Monday",\n        "Tuesday",\n        "Wednesday",\n        "Thursday",\n        "Friday"\n      ],\n      "opens": "05:00",\n      "closes": "01:00"\n    },\n    {\n      "@type": "OpeningHoursSpecification",\n      "dayOfWeek": [\n        "Saturday",\n        "Sunday"\n      ],\n      "opens": "05:00",\n      "closes": "24:00"\n    }\n  ],\n  "telephone": "+81-45-441-1111",\n  "url": "https://www.jreast.co.jp/estation/station/info.aspx?StationCd=111"\n}\n```\n\nこの例では、神奈川駅を表す `Place` タイプのオブジェクトを定義しています。`name` プロパティには駅名を、`address` プロパティには住所を、`geo` プロパティには緯度経度を、`openingHoursSpecification` プロパティには営業時間を、`telephone` プロパティには電話番号を、`url` プロパティには公式ウェブサイトのURLをそれぞれ指定しています。また、住所は `PostalAddress` タイプのオブジェクトで表現され、`addressLocality` プロパティには市区町村名、`addressRegion` プロパティには都道府県名、`postalCode` プロパティには郵便番号、`streetAddress` プロパティには番地以下の住所をそれぞれ指定しています。営業時間は `OpeningHoursSpecification` タイプのオブジェクトで表現され、`dayOfWeek` プロパティには曜日、`opens` プロパティには開店時間、`closes` プロパティには閉店時間をそれぞれ指定しています。'}]

example_formatter_template = """
フルーツ: {location}
色: {JSON}\n
"""
example_prompt = PromptTemplate(
    template=example_formatter_template,
    input_variables=["location", "JSON"]
)

few_shot_prompt = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
    prefix="あなたは与えられた単語に関してShcema.orgのJSON-LDを用いて記述するエージェントです。この時schema:location を使ってエンコードしてください",
    suffix="フルーツ: {input}\nJSON:",
    input_variables=["input"],
    example_separator="\n\n",

)

prompt_text = few_shot_prompt.format(input="武蔵浦和駅")
print(prompt_text)

llm = OpenAI(model_name="text-davinci-003")
print(llm(prompt_text))