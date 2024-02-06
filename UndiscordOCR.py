#https://github.com/vinicius-m1/UndiscordOCR.git
import discord
from PIL import Image
import pytesseract
import requests
import os.path
from configparser import ConfigParser
from datetime import datetime
intents = discord.Intents.default()
intents.message_content = True


config = ConfigParser()
config.read("config.ini")
config_data = config['default']
token = config_data['token']
channel_id = config_data['channel_id']
history_deletion = config_data['history_deletion']
store_flagged = config_data['store_flagged_messeges']

word = config_data['word']
word.replace(",","")

def words_in_string(word_list, text):
    return set(word_list).intersection(text.split())



async def delete_history():
    channel = client.get_channel(channel_id)
    messages = [message async for message in channel.history(limit=100000)]
    
    i =0
    for message in messages:
        #contents.append(message.content)
        
        print(i)
        i = i+1
        if message.attachments:
            url = message.attachments[0].url
            try:
                img_data = requests.get(url).content            
                
                filename = url.split('/')[-1]
                filename = filename.split('?', 1)[0]
                open(filename, 'wb').write(img_data) 
            except: 
                print("Error saving image") 
                continue
            
            try:
                text = pytesseract.image_to_string(filename) #OCR
            except: 
                print("Erro durante OCR")
                os.remove(filename)
                continue            

            print (text)
            if words_in_string(word, text):
                print("Detected blocked word! Deleting")
                await message.delete()
            else: os.remove(filename)
            




#WATCH FOR MESSAGES IN REAL TIME
class MyClient(discord.Client):
    async def on_ready(self):
        await MyClient.change_presence(status=discord.Status.invisible)
        print(f'Logged on as {self.user}!')


        if history_deletion == 'True':
            await delete_history()

    async def on_message(self, message):
        #if message.author.id == (1203429051226787890):
                     #await message.delete()   

        #print(f'Message from {message.author}: {message.content}')
        #with open('log.txt', 'a') as f:
            #f.write(f'{datetime.now()} {message.author}: {message.content} \n')
        if message.attachments:
            url = message.attachments[0].url
            img_data = requests.get(url).content
            filename = url.split('/')[-1]
            filename = filename.split('?', 1)[0]
            

            open(filename, 'wb').write(img_data)            

            print (bcolors.OKCYAN,"Processing attachments!",bcolors.ENDC)

            
            text = pytesseract.image_to_string(filename)
            print (bcolors.OKGREEN, "OCR readings:", bcolors.ENDC, text)
            
            
            if words_in_string(word, text):
                await message.delete()
                print (bcolors.WARNING, "Keyword found in OCR reading! Deleting chat message.", bcolors.ENDC)
                if store_flagged == 'False'
                    os.remove(filename)
            else: os.remove(filename)
            
                
        


client = MyClient(intents=intents)
client.run(token)

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

