import speech_recognition as sr
import pyttsx3


class Jarvis:
    def __init__(self, rate=125):
        self.engine = pyttsx3.init()
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

        self.set_rate(rate)

        self.said = []
        self.heard = []

    def set_rate(self, rate):
        self.speech_rate = rate
        self.engine.setProperty('rate', rate)

    def set_microphone(self, obj):
        self.microphone = obj

    def get_heard(self):
        return self.heard

    def get_said(self):
        return self.said

    def say(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

        self.said.append(text)
        if len(self.said) > 500:
                del self.said[:250]

    def listen(self, anf=True):
        with self.microphone as source:
            if anf:  # ambient noise filter
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = self.recognizer.listen(source)

        text = None
        try:
            text = self.recognizer.recognize_google(audio).lower()

            self.heard.append(text)
            if len(self.heard) > 500:
                del self.heard[:250]
        except sr.UnknownValueError:
            pass

        return text
            

def example():
    speaker = Jarvis()
    speaker.say('say something')
    speaker.say(speaker.listen())
    speaker.say('the end of example')


if __name__ == '__main__':
    example()
