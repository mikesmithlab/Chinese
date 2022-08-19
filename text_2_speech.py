import pyttsx3

voice_dict = {'en':0,
            'ch':2}


def text2speech(text, lang='en', card_id=None):
    engine = pyttsx3.init()
    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[voice_dict[lang]].id)
    engine.setProperty("rate",170)
    engine.say(text)
    #engine.save_to_file(text, "card_id" + '.mp3')
    engine.runAndWait()

def guess_english_or_chinese(text):
    for char in text:
        if ord(char) > 250:
            return 'ch'
    return 'en'



# convert this text to speech
text = "我是他的朋友"
text2 = "I can speak English"

text2speech(text, lang=guess_english_or_chinese(text))
text2speech(text2, lang=guess_english_or_chinese(text2))
