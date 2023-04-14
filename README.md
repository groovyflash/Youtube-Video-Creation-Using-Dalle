# Youtube-Video-Creation-Using-Dalle
Creates a video from a youtube video using a combination of Whisper (to find the words to the song), Chat GPT (to create the prompt) and Dalle2 to create the images. It creates a video for you and all you need is your openAI key

To use - 

Make sure you have python 3.9 or later

Clone the git repository

Install youtube dlp

https://github.com/yt-dlp/yt-dlp/wiki/Installation
or just like this
python3 -m pip install -U yt-dlp
pip install all the packages you dont have see below:

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

Enter your openapi key in the code (you can see in the first line of my code) where it says secret. You can find this at https://platform.openai.com/account/api-keys

Then just run the program using python.

If you want any additional features or notice any bug fixes let me know. Make sure your youtube link is the full link not abbreviated and not off of a playlist. Other than that you should be good to go! :)
