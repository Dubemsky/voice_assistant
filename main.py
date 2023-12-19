import openai
import pyttsx3
# This allows to convert text to speech
import speech_recognition as sr
import time

# allows to transcribe audio to text

openai.api_key = "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"
error1 = "I couldn't understand your request. Please try again"

engine = pyttsx3.init()

def audio_to_text(filename):
    recognizer = sr.Recognizer()
    # is required to perform speech recognition on the audio file
    with sr.AudioFile(filename) as source:
        # OPEN AUDIO FILE
        audio = recognizer.record(source)
        # TRANSCRIBING AUDIO TO TEXT

    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        speak("Try again")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")


def generate_response(prompt):
    # GENERATE RESPONSE BASED OF A GIVING PROMPT
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=400,
        n=1,
        stop=None,
        temperature=0.5
    )
    return response.choices[0].text


def speak(text):
    engine.say(text)
    engine.runAndWait()


def main():
    speaking = True
    while speaking:
        print("Hello, my name is vortex. If you need assistance, call my name")

        with sr.Microphone() as source:
            # RECORDING THE AUDIO
            recognizer = sr.Recognizer()
            audio = recognizer.listen(source)
            try:
                transcription = recognizer.recognize_google(audio)
                if transcription.lower() == "vortex":
                    filename = "input.wav"
                    speak("How may I be of assistance?")
                    with sr.Microphone() as source:
                        recognizer = sr.Recognizer()
                        source.pause_threshold = 1
                        audio = recognizer.listen(source, phrase_time_limit=None, timeout=None)
                        with open(filename, "wb") as f:
                            f.write(audio.get_wav_data())

                    text = audio_to_text(filename)
                    if text:
                        print(f"You: {text}")

                        response = generate_response(text)
                        print(f"Vortex: {response}")

                        speak(response)




            except sr.UnknownValueError:
                speak(error1)
            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition service; {e}")


if __name__ == "__main__":
    main()