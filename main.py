import record
import analysis_whisper
import response_groq
import speak_text
import finish_check


def main():
    history = None

    while True:
        #録音開始
        wav_data = record.record_audio()
        if wav_data is None:
            break

        #録音データを分析
        analysis_text = analysis_whisper.transcribe_audio(wav_data)
        if wav_data is None:
            break

        #終了するか確認
        if finish_check.text_word_check(analysis_text):
            break

        #AIの回答を作成
        ai_text, history = response_groq.generate_response(analysis_text, history)
        if ai_text is None:
            break

        print(ai_text) #debug

        #回答を読み上げる
        speak_text.speak(ai_text)

main()