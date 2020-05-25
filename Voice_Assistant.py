#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 01:07:18 2020

@author: sathvik
"""
import speech_recognition as sr
import os
#import sys
import re
import webbrowser
import smtplib
import requests
import subprocess
from pyowm import OWM
import youtube_dl
import vlc
import urllib
import urllib2
import json
from bs4 import BeautifulSoup as soup
from urllib2 import urlopen
import wikipedia
#import random
#from time import strftime

def myCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Say Something...!')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source,duration=1)
        audio = r.listen(source)
    try:
        command = r.recognize_google(audio).lower()
        print('You said: ' + command + '\n')
    except sr.UnknownValueError:
        print('....')
        command = myCommand();
    return command

def sofiaResponse(audio):
    print(audio)
    for line in audio.splitlines():
        os.system("say " + audio)

def assistant(command):
    "if statements for executing commands"
#open subreddit Reddit
    if 'open reddit' in command:
        reg_ex = re.search('open reddit (.*)',command)
        url = 'https://www.reddit.com/'
        if reg_ex:
            subreddit = reg_ex.group(1)
            url = url + 'r/' + subreddit
        webbrowser.open(url)
        sofiaResponse('The Reddit content has been opened for you.')
    elif 'shutdown' in command:
            sofiaResponse('Bye Bye. Have a nice day')
    elif 'open' in command:
        reg_ex = re.search('open(.+)',command)
        if reg_ex:
            domain = reg_ex.group(1)
            domain = domain.strip()
            print(domain)
            url = 'https://www.' + domain
            webbrowser.open(url)
            sofiaResponse('The website you hae requested has been opened for you sir.')
        else:
            pass
    elif 'help me' in command:
        sofiaResponse(""" You can use these commands and I'll help you out:
            1. Open reddit subreddit : Opens the subreddit in default browser.
            2. Open any website
            3. Send email/email : Follow up questions such as recipient name, content will be asked in order.
            4. Current weather in {cityname} : Tells you the current condition and temperature
            5. Hello
            6. Play a video : Plays song in your VLC media player
            7. change wallpaper : Change desktop wallpaper
            8. news for today : reads top news of today
            9. time : Current system time
            10. top stories from google news (RSS feeds)
            11. tell me about anything
            """)
    elif 'joke' in command:
        res = requests.get('https://icanhazdadjoke.com/',
                           headers = {"Accept":"application/json"})
        if res.status_code == requests.codes.ok:
            sofiaResponse(str(res.json()['joke']))
        else:
            sofiaResponse('oops! I ran out of jokes')
    elif 'news for today' in command:
        try:
            news_url = "https://news.google.com/news/rss"
            Client=urlopen(news_url)
            xml_page=Client.read()
            Client.close()
            soup_page=soup(xml_page,"xml")
            news_list=soup_page.findAll("item")
            for news in news_list[:15]:
                sofiaResponse(news.title.text.encode('utf-8'))
        except Exception as e:
                print(e)
    elif 'current weather' in command:
        reg_ex = re.search('current weather in (.*)', command)
        if reg_ex:
            city = reg_ex.group(1)
            owm = OWM(API_key='ab0d5e80e8dafb2cb81fa9e82431c1fa')
            obs = owm.weather_at_place(city)
            w = obs.get_weather()
            k = w.get_status()
            x = w.get_temperature(unit='celcius')
            sofiaResponse('Current weather in %s is %s. The maximum temperatue is %0.2f and the minimum temperature is %0.2f degree celcius' % (city,k,x['temp_max'],x['temp_min']))
    elif 'time' in command:
        import datetime
        now = datetime.datetime.now()
        sofiaResponse('Current time is %d hours %d minutes'%(now.hour,now.minute))
    elif 'email' in command:
        sofiaResponse('Who is the recipient?')
        recipient = myCommand()
        if 'rajat' in recipient:
            sofiaResponse('What should I say to him?')
            content = myCommand()
            mail = smtplib.SMTP('smtp.gmail.com',587)
            mail.ehlo()
            mail.starttls()
            mail.login('your_email_address','your_password')
            mail.sendmail('sender_email','receiver_email',content)
            mail.close()
            sofiaResponse('Email has been sent successfully. You can check your inbox.')
        else:
            sofiaResponse('I don\'t know what you mean!')
    elif 'launch' in command:
        reg_ex = re.search('launch (.*)',command)
        if reg_ex:
            appname = reg_ex.group(1)
            appname1 = appname+".app"
            subprocess.Popen(["open","-n","/Application/"+appname1], stdout=subprocess.PIPE)
            sofiaResponse('I have launched the desired application')
    elif 'play me a song' in command:
        path = '/Users/sathvik/Downloads/videos/'
        folder = path
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(e)
        sofiaResponse('What song shall I play?')
        mysong = myCommand()
        if mysong:
            flag = 0
            url = "http://www.youtube.com/results?search_query=" + mysong.replace(' ','+')
            response = urllib2.urlopen(url)
            html = response.read()
            soup1 = soup(html,"lxml")
            url_list = []
            for vid in soup1.findAll(attrs={'class':'yt-uix-tile-link'}):
                if ('https://www.youtube.com' + vid['href']).startswith("https://www.youtube.com/watch?v="):
                    flag = 1
                    final_url = 'https://www.youtube.com' + vid['href']
                    url_list.append(final_url)
                    url = url_list[0]
                    ydl_opts = {}
                    os.chdir(path)
                    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                        ydl.download([url])
                        vlc.play(path)
            if flag == 0:
                sofiaResponse('I have not found anything in Youtube')
    elif 'change wallpaper' in command:
        folder = '/Users/sathvik/Documents/wallpaper/'
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(e)
        api_key = 'fd66364c0ad9e0f8aabe54ec3cfbed0a947f3f4014ce3b841bf2ff6e20948795'
        url = 'https://api.unsplash.com/photos/random?client_id=' + api_key
        f = urllib2.urlopen(url)
        json_string = f.read()
        f.close()
        parsed_json = json.loads(json_string)
        photo = parsed_json['urls']['full']
        urllib.urlretrieve(photo,"/Users/sathvik/Documents/wallpaper/a")
        subprocess.call(["killall Dock"], shell=True)
        sofiaResponse('Wallpaper changed successfully')
    elif 'tell me about' in command:
        reg_ex = re.search('tell me about (.*)', command)
        try:
            if reg_ex:
                topic = reg_ex.group(1)
                ny = wikipedia.page(topic)
                sofiaResponse(ny.content[:500].encode('utf-8'))
        except Exception as e:
            print(e)
            sofiaResponse(e)
    sofiaResponse('Hey, i am Sofia and I am your personal voice assistant, Please give a command or say "help me and I will tell you what all I can do for you.')
    while True:
        assistant(myCommand())
