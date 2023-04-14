import os
import subprocess
import ffmpeg
import os
import openai
import requests
import glob, os
import webvtt
import yt_dlp
from nltk import pos_tag
from moviepy.editor import *


secret = ""#Enter your API Key in the spaces
message = input('Enter the full youtube URL that you would like to create a video of here: ')
lyrics = input('Enter the number of lyrics that you would like to create into a picture - suggestion ~15 for rap ~8 for rock/pop ')
lyrics = int(lyrics)
style = input('Enter the style of art you would like (recommendation - digital) ')
opening = input('Enter the opening prompt or the prompt when there could be something too explicit (sometimes I do the name of the artist) ')
directory = os.getcwd()
print(directory)


def createclip(image, start, duration):
    clips = clips = [ImageClip(image + '.jpg').set_duration(duration)]
    concat_clip = concatenate_videoclips(clips, method="compose")
    audioclip = AudioFileClip("output.wav").subclip(start, (start+duration))
    videoclip = concat_clip.set_audio(audioclip)
    videoclip.write_videofile(image + ".mp4", fps=24)


def parsescript(prompt):
    test = ['JJ','JJR','JJS','NN','NNS','NNPS','RB','RBR','RBS','VB','VBG','VBN','VBP','VBD','VBZ']
    export = ""
    text = prompt.split()
    tokens_tag = pos_tag(text)
    for l in tokens_tag:
        if l[1] in test:
            export = export + " " + l[0]
    return export

def createprompt(lyrics):
    messages = [
    {"role": "system", "content" : "text summerizer in terms of a picture"}
    ]
    messages.append({"role": "user", "content": "I have the following lyrics I would like to create a digital style image with Dalle2 could you recommend a prompt? limit your response to in 12 words or less - " + lyrics})

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
        )

    chat_response = completion.choices[0].message.content
    chat_response = chat_response.replace('"','')
    return chat_response

def createimage(prompt, name, message):
    secret = "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"
    secret = secret
    openai.api_key=secret
    openai.Model.list()

    response = openai.Image.create(
        prompt = prompt.replace('"','')  + "," +  style,
        n = 2,
        size = "512x512"
    )
    image_url = response['data'][0]['url']
    print(image_url)

    img_data = requests.get(image_url).content
    with open(directory + "/"  + message[30:] + "/" + name +'.jpg', 'wb') as handler:
        handler.write(img_data)

def getvideo(video, message):

    ydl_opts = {
    'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',
    'outtmpl': directory + "/" + message[30:] + '/test.mp4'
    }
# create a YoutubeDL object
    ydl = yt_dlp.YoutubeDL(ydl_opts)

# download the video
    ydl.download([video])


    INPUT_FILE = directory + "/" + message[30:] + "/test.mp4"
    OUTPUT_FILE = directory + "/" + message[30:] + "/output.wav"

    (
    ffmpeg.input(INPUT_FILE).output(OUTPUT_FILE, acodec='pcm_s16le', y='-y').run()
    )


def getprompts(message):
    count = 0
    duration = 0
    prompt = ""
    clips = []
    NAME = opening
    NAME = createprompt(NAME)
    createimage(NAME, NAME, message)
    clips.append(ImageClip(directory + "/" + message[30:] + "/" + NAME + '.jpg').set_duration(0.5))
    export = ""
    start = 0

    for file in glob.glob(directory + "/" + message[30:] + "/" + "*.vtt"):
        for caption in webvtt.read(file):
            print(caption.start)
            print(caption.end)
            print(caption.text)

            export = caption.text
            
            for e in export:
            # print(e)
                if e.isspace():
                    if count <lyrics:
                        count = count + 1
                        print(count)
                if count==lyrics:
                    prompt = prompt + " " + export
                    hh, mm, ss = caption.end.split(':')
                    final = int(hh) * 3600 + int(mm) * 60 + float(ss)
                    duration = duration + (final - start)
                    break
                # print(analyzer)
            if count == lyrics:
                # print("prompt " + prompt)
                print(duration)
                try:
                    print(prompt)
                    prompt = createprompt(prompt)
                    print("prompt " + prompt)
                    createimage(prompt, prompt, message)
                    clips.append(ImageClip(directory + "/" + message[30:] + "/" +prompt + '.jpg').set_duration(duration))
                except:
                    createimage(NAME, NAME, message)
                    clips.append(ImageClip(directory + "/" + message[30:] + "/" +NAME + '.jpg').set_duration(duration))
                duration = 0
                prompt = ""
                count = 0
            else:
                prompt = prompt + export
                hh, mm, ss = caption.end.split(':')
                final = int(hh) * 3600 + int(mm) * 60 + float(ss)
                duration = duration + (final - start)
            hh, mm, ss = caption.end.split(':')
            start = int(hh) * 3600 + int(mm) * 60 + float(ss)
        concat_clip = concatenate_videoclips(clips, method="compose")
        audioclip = AudioFileClip(directory + "/" + message[30:] +"/output.wav")
        videoclip = concat_clip.set_audio(audioclip)
        videoclip.write_videofile(directory + "/" + message[30:] +"/final.mp4", fps=24)
        folder_path = directory + "/" + message[30:]

def createvideo(message):  
    try:
        os.mkdir(directory + "/"  + message[30:])
    except:
        print("didnt make directory")
    print(message)
    cmd_str = f'yt_whisper "{message}" --model medium'
    subprocess.run(cmd_str, shell=True, cwd=directory + "/"  + message[30:])
    getvideo(message, message)
    getprompts(message)


createvideo(message)


