from groq import Groq
import client_manager

history = None #初期化用
def generate_response(user_text, history=None):
    """
    user_text: Whisperで取得したテキスト
    history: 過去の会話履歴（リスト）
    """
    # Groq API クライアント
    key = client_manager.api_manager("groq_api")
    client = Groq(api_key = key)

    if history is None:
        history = []

    # 会話履歴にユーザー発話を追加
    history.append({"role": "user", "content": user_text})

    # Groqへ送信
    response = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=history,
    temperature=0.7
    )

    # 応答テキスト
    ai_text = response.choices[0].message.content

    # 会話履歴にAIの返答を追加
    history.append({"role": "assistant", "content": ai_text})

    return ai_text, history
