import record
import analysis_whisper
import response_groq

COUNT_MAX = 10

def main():
    history = None
    cnt = 0

    while cnt < COUNT_MAX:
        cnt += 1
        #録音開始
        print("wav data")
        wav_data = record.record_audio()

        #録音データを分析
        print("analysis")
        analysis_text = analysis_whisper.transcribe_audio(wav_data)

        ai_text, history = response_groq.generate_response(analysis_text, history)

        print(ai_text)

main()