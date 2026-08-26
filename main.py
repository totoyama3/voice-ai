import record
import analysis_whisper
import response_groq
import speak_text
import finish_check

COUNT_MAX = 10

def main():
    history = None
    cnt = 0

    while cnt < COUNT_MAX:
        cnt += 1
        #録音開始
        wav_data = record.record_audio()

        #録音データを分析
        analysis_text = analysis_whisper.transcribe_audio(wav_data)

        #終了するか確認
        if finish_check.text_word_check(analysis_text):
            break

        #AIの回答を作成
        ai_text, history = response_groq.generate_response(analysis_text, history)

        print(ai_text) #debug

        #回答を読み上げる
        speak_text.speak(ai_text)

main()