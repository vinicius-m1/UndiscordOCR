#https://github.com/vinicius-m1/UndiscordOCR.git
import discord
from PIL import Image
import pytesseract
import requests
import os.path
import asyncio
from configparser import ConfigParser
from datetime import datetime
intents = discord.Intents.default()
intents.message_content = True



if not os.path.isdir('./images'): os.mkdir('./images')

config = ConfigParser()
config.read("config.ini")
config_data = config['default']
token = config_data['token']
channel_id = int(config_data['channel_id'])
history_deletion = config_data['history_deletion']
store_flagged = config_data['store_flagged_messeges']
word = config_data['word']
word = word.split(",")

def words_in_string(word_list, text):
    return set(word_list).intersection(text.split())



# COLORED TEXT    
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


async def delete_history():
    
    print (f"BLOCKED WORDS: {word}")
    channel = client.get_channel(channel_id)
    i =0
    last_message = None
    while True:
    #messages = [message async for message in channel.history(limit=1000)]
        async for message in channel.history(limit = 100, before=last_message):
        
            i = i+1
            last_message = message.created_at

            if message.attachments:
            
                url = message.attachments[0].url
                filename = url.split('/')[-1]
                filename = filename.split('?', 1)[0]
                
                if filename.endswith(".png") or filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".webp"):

                    try:
                        fileLocation = os.path.join('./images', filename)
                        img_data = requests.get(url).content
                                
                        open(fileLocation, 'wb').write(img_data) 
                    except: 
                        print(bcolors.ENDC,"Error saving image",bcolors.ENDC) 
                        continue
            
                    try:
                        text = pytesseract.image_to_string(fileLocation) #OCR
                    except: 
                        print(bcolors.WARNING, "OCR Error, probably attachment not an image:",bcolors.ENDC,filename)
                        os.remove(fileLocation)
                        continue            

                    
                    if words_in_string(word, text):
                        print(bcolors.WARNING, "Keyword found in OCR reading! Deleting chat message.", bcolors.ENDC)
                        print (text)
                        await message.delete()
                    else: os.remove(fileLocation)

        
        print(f"{i} messages searched until now. last message was: {last_message}")
        


#WATCH FOR MESSAGES IN REAL TIME
class MyClient(discord.Client):
    async def on_ready(self):


        print(f'Logged on as {self.user}!')        

        if history_deletion == 'True':
            await delete_history()

    async def on_message(self, message):
        
        if message.attachments:
            url = message.attachments[0].url
            img_data = requests.get(url).content
            filename = url.split('/')[-1]
            filename = filename.split('?', 1)[0]
            fileLocation = os.path.join('./images', filename)
            
            open(fileLocation, 'wb').write(img_data)            

            print (bcolors.OKCYAN,"Processing attachments!",bcolors.ENDC)

            
            text = pytesseract.image_to_string(fileLocation)
            print (bcolors.OKGREEN, "OCR readings:", bcolors.ENDC, text)
            
            
            if words_in_string(word, text):
                await message.delete()
                print (bcolors.WARNING, "Keyword found in OCR reading! Deleting chat message.", bcolors.ENDC)
                if store_flagged == 'False':
                    os.remove(fileLocation)
            else: os.remove(fileLocation)
            
                
        


client = MyClient(intents=intents)
client.run(token)


