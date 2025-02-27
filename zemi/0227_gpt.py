import openai

class ChatBot:
    def __init__(self):
        self.client = openai.OpenAI()  # 新しいAPIのクライアントを作成

    def response(self, user_input):
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",  # モデルを指定
                messages=[{"role": "user", "content": user_input}]
            )
            return response.choices[0].message.content  # 応答を取得
        except openai.OpenAIError as e:
            return f"エラーが発生しました: {str(e)}"

if __name__ == "__main__":
    chatbot = ChatBot()
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            break
        reply = chatbot.response(user_input)
        print(f"ChatGPT: {reply}")
