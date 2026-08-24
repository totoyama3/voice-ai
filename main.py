import record
import analysis_whisper
import response_groq

def main():
    #録音開始
    print("wav data")
    wav_data = record.record_audio()

    #録音データを分析
    print("analysis")
    analysis_text = analysis_whisper.transcribe_audio(wav_data)

    ai_text, history = response_groq.generate_response(analysis_text)

    print(ai_text)

main()