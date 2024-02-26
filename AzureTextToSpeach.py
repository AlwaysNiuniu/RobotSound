# FileName : AzureTextToSpeach.py
# DATE: 2023-10-11
# Time : 17:53
# Author: MIO
# -*- coding: utf-8 -*-
import os
from os.path import exists
import azure.cognitiveservices.speech as speechsdk


def main():
    # This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"
    speech_config = speechsdk.SpeechConfig(subscription=os.environ.get('SPEECH_KEY'), region=os.environ.get('SPEECH_REGION'))
    audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)

    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

    with open('robotlwr.xml', 'r', encoding='utf-8') as s:
        ssml = s.read()

    speech_synthesis_result = speech_synthesizer.speak_ssml_async(ssml).get()


    if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Speech synthesized for text success")
    elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_synthesis_result.cancellation_details
        print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            if cancellation_details.error_details:
                print("Error details: {}".format(cancellation_details.error_details))
                print("Did you set the speech resource key and region values?")

    # 保存文件
    if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        file_name = input('文件名是什么？(直接回车取消保存)')
        if file_name != '':
            # 保存生成的语音到文件
            audio_data = speech_synthesis_result.audio_data
            file_save_path = './AzureAudioSave/babysound'#保存在babysound文件夹里
            if not exists(file_save_path):
                os.mkdir(file_save_path)
            with open(f"{file_save_path}/{file_name}.flac", "wb") as audio_file:
                audio_file.write(audio_data)
    stream = speechsdk.AudioDataStream(speech_synthesis_result)
    stream.save_to_wav_file("./output.wav")
    print("文件已保存！")


if __name__ == '__main__':
    main()
