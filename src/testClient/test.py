
import os
import requests
import azure.cognitiveservices.speech as speechsdk


def speech_synthesis_to_mp3_file(token, region):
    """performs speech synthesis to a mp3 file"""
    # Creates an instance of a speech config with authorization token and service region.
    # https://learn.microsoft.com/en-us/python/api/azure-cognitiveservices-speech/azure.cognitiveservices.speech.speechconfig?view=azure-python
    speech_config = speechsdk.SpeechConfig(auth_token=token, region=region)
    # Sets the synthesis output format.
    # The full list of supported format can be found here:
    # https://docs.microsoft.com/azure/cognitive-services/speech-service/rest-text-to-speech#audio-outputs
    speech_config.set_speech_synthesis_output_format(speechsdk.SpeechSynthesisOutputFormat.Audio16Khz32KBitRateMonoMp3)
    # Creates a speech synthesizer using file as audio output.
    # Replace with your own audio file name.
    file_name = "outputaudio.mp3"
    file_config = speechsdk.audio.AudioOutputConfig(filename=file_name)
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=file_config)

    # Receives a text from console input and synthesizes it to mp3 file.
    print("Now synthesizing the text to mp3 file.")

    text = 'Why, ’tis a loving and a fair reply. Be as ourself in Denmark.—Madam, come. This gentle and unforced accord of Hamlet Sits smiling to my heart, in grace whereof. No jocund health that Denmark drinks today. But the great cannon to the clouds shall tell, And the King’s rouse the heaven shall bruit again, Respeaking earthly thunder. Come away.'
    result = speech_synthesizer.speak_text_async(text).get()
    # Check result
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Speech synthesized for text [{}], and the audio was saved to [{}]".format(text, file_name))
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))


def main():
    url = 'http://127.0.0.1:5000/token'
    token = ''
    response = requests.get(url)
    if response.status_code == 200:
        token = response.json()['token']
    else:
        return
        
    speech_synthesis_to_mp3_file(token=token, region='southeastasia')


if __name__ == "__main__":
   main()
