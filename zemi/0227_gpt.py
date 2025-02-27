import openai

class AIChat:
    def __init__(self):
        # ※冒頭で作成したopenai の APIキーを設定してください
        openai.api_key = "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"

    def response(self, user_input):
        # openai の GPT-3 モデルを使って、応答を生成する
        response = openai.Completion.create(
            engine="text-davinci-003", # text-davinci-003 を指定した方がより自然な文章が生成されます
            prompt=user_input,
            max_tokens=1024,
            temperature=0.5, # 生成する応答の多様性
        )

        # 応答のテキスト部分を取り出して返す
        return response['choices'][0]['text']
