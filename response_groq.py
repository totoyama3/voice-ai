from groq import Groq
import secret_manager

METHOD = "response"
GROQ_PROMPT = """
あなたはDiscordでユーザーと自然に会話するAIアシスタントです。

【基本ルール】
・日本語で会話する
・友達と話すような自然で親しみやすい口調にする
・ユーザーの直前の発言を必ず踏まえて返答する
・過去の会話内容も考慮して返答する
・会話の流れを無視して突然別の話題を始めない
・ユーザーの発言に直接関係する返答をする
・雑談では説明しすぎず、会話を続けることを優先する
・回答は基本的に1〜3文程度にする
・音声で読み上げるため、自然な話し言葉を使う
・箇条書きや特殊な記号はなるべく使わない

【会話のルール】
・質問されたら、その質問に答える
・ユーザーが選択肢を提示したら、その選択肢から自然に選ぶ
・ユーザーが話題を振ったら、その話題について反応する
・ユーザーが何かを報告したら、まずその内容に反応する
・会話を続けるために質問する場合は、直前の話題に関係する質問をする
・「やっほー」などの定型的な挨拶を毎回入れない
・ユーザーの発言と関係のない話題に突然切り替えない

【重要】
回答を作るときは、まず「ユーザーは今、何について話しているのか」を考えてください。
その内容に直接反応する回答を生成してください。
"""

def generate_response(user_text, history=None):

    # Groq API クライアント
    try:
        key = secret_manager.api_manager("groq_api")
        client = Groq(api_key=key)
    except Exception as e:
        print(f"{METHOD}のクライアント取得でエラー発生しました")
        print(f"エラー内容：{e}")
        return None, history

    if history is None:
        history = []

    # 今回のユーザー発話を履歴に追加
    history.append({
        "role": "user",
        "content": user_text
    })

    # メッセージを作成
    messages = [
        {
            "role": "system",
            "content": GROQ_PROMPT
        }
    ]

    # 過去の会話＋今回の発話
    messages.extend(history)

    # Groqへ送信
    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=messages,
            temperature=0.7
        )
    except Exception as e:
        print(f"{METHOD}のAI処理でエラー発生しました")
        print(f"エラー内容：{e}")
        return None, history

    # 応答テキスト
    ai_text = response.choices[0].message.content

    # AIの返答を履歴に追加
    history.append({
        "role": "assistant",
        "content": ai_text
    })

    return ai_text, history