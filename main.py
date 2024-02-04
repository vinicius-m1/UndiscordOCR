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

word = ['BANSOLA', 'Bansola', 'bansola','8ur3j85hy98']

def words_in_string(word_list, text):
    return set(word_list).intersection(text.split())



async def delete_history():
    channel = client.get_channel(849794290317525014)
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
        print(f'Logged on as {self.user}!')
        await delete_history()

    async def on_message(self, message):
        #if message.author.id == (1203429051226787890):
                     #await message.delete()   

        print(f'Message from {message.author}: {message.content}')
        #with open('log.txt', 'a') as f:
            #f.write(f'{datetime.now()} {message.author}: {message.content} \n')
        if message.attachments:
            url = message.attachments[0].url
            img_data = requests.get(url).content
            filename = url.split('/')[-1]
            filename = filename.split('?', 1)[0]
            

            open(filename, 'wb').write(img_data)            

            #print ("the last message had attachments!")

            
            text = pytesseract.image_to_string(filename)
            print (text)
            os.remove(filename)
            if words_in_string(word, text):
                await message.delete()
            
                
        




client = MyClient(intents=intents)
client.run(token)


