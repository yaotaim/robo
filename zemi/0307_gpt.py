from openai import OpenAI
import os

# OpenAI APIのモデル名を設定
MODEL = "gpt-4o-mini"

# OpenAI APIのクライアントを作成
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# gpt.txt からシステムメッセージを読み込む
with open("chat.txt", "r", encoding="utf-8") as f:
    system_message = f.read().strip()

# ユーザーの入力を取得
user_input = input("You: ")

# OpenAIのAPIを使ってチャットのレスポンスを生成
completion = client.chat.completions.create(
    model=MODEL,
    messages=[
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_input}
    ]
)

# AIの応答を出力
print("Assistant: " + completion.choices[0].message.content)
