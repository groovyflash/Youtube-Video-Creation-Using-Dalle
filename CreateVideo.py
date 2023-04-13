import openai
import glob
import webvtt
import os

secret = #enter your key here
openai.api_key = secret


def createprompt(lyrics):
    messages = [
    {"role": "system", "content" : "text summerizer in terms of a picture"}
    ]
    messages.append({"role": "user", "content": "I have the following lyrics I would like to create a digital style image with Dalle2 could you recommend a prompt? desired format prompt: '' - " + lyrics})

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
        )

    chat_response = completion.choices[0].message.content
    print(chat_response)
    return chat_response

def getprompts():
    count = 0
    duration = 0
    prompt = ""
    clips = []
    # NAME = "Juice Wrld"
    # createimage(NAME, NAME, message)
    # clips.append(ImageClip("C:/Users/fisch/OneDrive/Desktop/"+ message[30:] + "/" + NAME + '.jpg').set_duration(0.5))
    export = ""
    start = 0
    for file in glob.glob("C:/Users/fisch/OneDrive/Desktop/" + "*.vtt"):
        for caption in webvtt.read(file):
            # print(caption.start)
            # print(caption.end)
            # print(caption.text)

            export = caption.text
            
            for e in export:
            # print(e)
                if e.isspace():
                    if count <10:
                        count = count + 1
                        print(count)
                if count==10:
                    prompt = prompt + " " + export
                    hh, mm, ss = caption.end.split(':')
                    final = int(hh) * 3600 + int(mm) * 60 + float(ss)
                    duration = duration + (final - start)
                    break
                # print(analyzer)
            if count == 10:
                # print("prompt " + prompt)
                # print(duration)
                try:
                    createprompt(prompt)

                    # createimage(prompt, prompt, message)
                    # clips.append(ImageClip("C:/Users/fisch/OneDrive/Desktop/"+ message[30:] + "/" +prompt + '.jpg').set_duration(duration))
                except:
                    print("did not work")
                    # createimage(NAME, NAME, message)
                    # clips.append(ImageClip("C:/Users/fisch/OneDrive/Desktop/"+ message[30:] + "/" +NAME + '.jpg').set_duration(duration))
                
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
getprompts()