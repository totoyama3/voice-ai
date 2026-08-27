from groq import Groq
import secret_manager

METHOD = "response"
history = None #初期化用

def generate_response(user_text, history=None):
    # Groq API クライアント
    try:
        key = secret_manager.api_manager("groq_api")
        client = Groq(api_key = key)
    except Exception as e:
        print(f"{METHOD}のクライアント取得でエラー発生しました")
        print(f"エラー内容：{e}")
        return None, history

    if history is None:
        history = []

    # 会話履歴にユーザー発話を追加
    history.append({"role": "user", "content": user_text})

    # Groqへ送信
    try:
        response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=history,
        temperature=0.7
        )
    except Exception as e:
        print(f"{METHOD}のAI処理でエラー発生しました")
        print(f"エラー内容：{e}")
        return None, history

    # 応答テキスト
    ai_text = response.choices[0].message.content

    # 会話履歴にAIの返答を追加
    history.append({"role": "assistant", "content": ai_text})

    return ai_text, history
