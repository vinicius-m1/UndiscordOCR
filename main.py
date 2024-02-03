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
word2 = config_data['word2']
word = config_data['word']


class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
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

            #tentar sem salvar no pc
            text = pytesseract.image_to_string(filename)
            print (text)
            os.remove(filename)
            if (word in text) or (word2 in text):
                await message.delete()
            
                
        




client = MyClient(intents=intents)
client.run(token)

