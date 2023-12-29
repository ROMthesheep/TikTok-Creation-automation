from moviepy.editor import *
from moviepy.video.fx.crop import crop
import os
from tiktok_voice_by_oscie57 import *
from private import SESSION_KEY
import requests
from bs4 import BeautifulSoup
import whisper_timestamped as whisper
import glob
import math

text = "I desperately need advice. In the past I was the one that committed infidelity just for some pretext. My wife and I came along way, even being separated for almost a year, but we came to a point where we wanted to make our relationship work for our almost 2 year old son. During our separation, she slept with 4 men in the span of two weeks one of those being unprotected. This was tough for me to get over, but because of the love I had for her and me wanting my family I found a way to look past all of that. During our separation, I was with other people. It was two people that she also knows about and she forgive me for. Our separation lasted about a year and ended around August of this year. About three weeks ago, my wife calls me and says that she went to get a check up. It turns out that she has chlamydia. I didn't sleep with anyone unprotected, but she did. This was tough to hear, but I decided to go ahead and take the necessary treatment, and still continue to live with her and try to work past this. Well, on Christmas day, I ended up seeing a text message on her phone saying That this person was thinking about her. After questioning her and actually calling this person on FaceTime and seeing their face because they thought it would be her on the phone. It turns out that she slept with one of the people that she had unprotected sex with during our separation again about two months ago, and never told me. This is also more than likely the person that she got the STD from, and gave it to me. I found all of this out on Christmas day while my son was opening his gifts. I'm stuck because to this point we have gotten through so much together. Now she is saying that because of a big fight that we had during that time that is why she decided to have sex with this person after they reached out to her. Now, keep in mind, that we already told each other that we will block and delete everyone from that time of seperation In our past. But somehow they found a way to get connected. She is very apologetic and saying that she wouldn't have done it if we were going through good times and we didn't have that big argument. She also tried to bring up my infidelity in the past as justification to not take accountability for this incident. The truth is if she didn't tell me about the std and if I didn't find out about this text I would have never known. I am thinking that we have still been married during this entire time. After all of the heartbreak we went through you still decided to have sex with this man, knowing what the consequences would be. There was no care for my health no care for the health of our son. You just let him have sex with you unprotected. I need some advice. As a person who was once the one that was caught cheating in the past (just talking on dating apps, is it time to just call this marriage quits and look forward to the healing process. Or does she deserve another chance after giving me a STD after cheating?"
if text[-1] == ".":
   text = text[:-1]
texts = text.split(".")
audios = []
audioFiles = []
for x in range(len(texts)):
  file = f"audios/output_{x}.mp3"
  tts(session_id= SESSION_KEY,
      req_text= texts[x],
      # text_speaker="es_002",
      filename= file)
  audios.append(AudioFileClip(file))

fullAudio = concatenate_audioclips([audio for audio in audios])
fullAudio.write_audiofile("fullAudio.mp3")

audioDuration = math.floor(AudioFileClip("fullAudio.mp3").duration) + 2
videoDuration = math.floor(VideoFileClip("videos/video.mp4").duration)
start = random.randint(0, videoDuration-audioDuration)

backVideo = VideoFileClip("videos/video.mp4").subclip(start, start + audioDuration)
(x,y) = backVideo.size
backVideo = crop(clip=backVideo,
                 width=480,
                 height=720,
                 x_center=x/2,
                 y_center=y/2)
backVideo.audio = AudioFileClip("fullAudio.mp3")

# Subs:
model = whisper.load_model("base")
result = whisper.transcribe(model,"fullAudio.mp3")
subs = []
subs.append(backVideo)
for segment in result["segments"]:
   for word in segment["words"]:
      text = word["text"]
      start = word["start"]
      end = word["end"]
      label = TextClip(txt=text,
                       fontsize=72,
                       font="Arial",
                       stroke_width=2,
                       stroke_color="black",
                       color="white")
      label = label.set_start(start).set_end(end).set_pos(("center","center"))
      subs.append(label)

print("Renderizado final")
finalVideo = CompositeVideoClip(subs)
finalVideo.write_videofile("tiktoks/output.mp4")

# Cleaning

audioFiles = glob.glob('audios/*')
for f in audioFiles:
    os.remove(f)
os.remove("fullAudio.mp3")

