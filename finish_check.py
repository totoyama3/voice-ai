
FINISH_WORD = ["終わり", "終了"]
               
def text_word_check(text):
    if text in FINISH_WORD:
        return True
    return False