import record
import analysis_whisper
import response_groq
import speak_text
import finish_check
import discord_bot

def main(wav_data):
    history = None

    """
    #録音開始
    wav_data = record.record_audio()
    if wav_data is None:
        break
    """

    #録音データを分析
    analysis_text = analysis_whisper.transcribe_audio(wav_data)
    if analysis_text is None:
        return
    print(f"音声解析結果：{analysis_text}")

    #終了するか確認
    if finish_check.text_word_check(analysis_text):
        return

    #AIの回答を作成
    ai_text, history = response_groq.generate_response(analysis_text, history)
    if ai_text is None:
        return

    print(f"回答結果：{ai_text}") #debug

    #回答のwavデータを作成する
    audio_data = speak_text.create_discord_voice(ai_text)

    #Discordでwavデータを再生する
    discord_bot.play_audio(audio_data)


def discord_start():
    discord_bot.client_run(main)
discord_start()