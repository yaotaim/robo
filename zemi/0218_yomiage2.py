import pyttsx3

# 初期化
engine = pyttsx3.init()

# 音声のスピード調整
rate = engine.getProperty('rate')
print('デフォルトの音声スピード: {}'.format(rate))
engine.setProperty('rate', 25)

# 音量調整
engine.setProperty('volume', 2.0) # デフォルトは1.0
volume = engine.getProperty('volume')
print('現在のボリューム: {}'.format(volume))

# 音声を「滑らかな女性」の方に設定
voices = engine.getProperty('voices')
#engine.setProperty('voice' ,'japanese', voices[1].id)
engine.setProperty('voice' ,'japanese')

while True:
    input_text = input('入力: ')
    engine.say(input_text)
    if input_text == 'q':
        engine.runAndWait()
        break
    else:
        engine.runAndWait()