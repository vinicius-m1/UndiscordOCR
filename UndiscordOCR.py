#https://github.com/vinicius-m1/UndiscordOCR.git
import discord
from PIL import Image
from PIL import ImageFile
import pytesseract
#import sys
import requests
import os.path
import asyncio
import shutil
from io import BytesIO
import pickle
from configparser import ConfigParser
from datetime import datetime
intents = discord.Intents.default()
intents.message_content = True
ImageFile.LOAD_TRUNCATED_IMAGES = True 



if not os.path.isdir('./images'): 
    os.mkdir('./images')
    os.mkdir('./images/flagged')


config = ConfigParser()
config.read("config.ini")
config_data = config['default']
token = config_data['token']
lang_ocr = config_data['lang_ocr']
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


def save_to_file(variable):
    with open("last_message.pickle", 'wb') as handle:
        pickle.dump(variable,handle, protocol=pickle.HIGHEST_PROTOCOL)

def load_from_file():
    with open('last_message.pickle', 'rb') as handle:
         return(pickle.load(handle))


async def OCR(data):
    return (pytesseract.image_to_string(Image.open(BytesIO(data)),lang=lang_ocr, timeout=100)) #OCR 


async def delete_history():


    if not os.path.isfile('last_message.pickle'):
        print ("Creating save file for last message.")
        open('last_message.pickle', 'a').close()
        save_to_file(datetime.now())
    
    print (f"BLOCKED WORDS: {word}")
    channel = client.get_channel(channel_id)
    i =0

    while True:
        last_message = load_from_file();
        async for message in channel.history(limit = 100, before=last_message):
        
            #i = i+1
            last_message = message.created_at
            
            await asyncio.sleep(0) #testing
            if message.attachments:
            
                url = message.attachments[0].url
                filename = url.split('/')[-1]
                filename = filename.split('?', 1)[0]
                
                await asyncio.sleep(0) #testing
                if filename.endswith(".png") or filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".webp"):

                    try:
                        img_data = requests.get(url).content                             
                        await asyncio.sleep(0) #testing
                    except Exception as err: 
                        print(bcolors.FAIL,"Error getting content!",bcolors.ENDC, err) 
                        continue
            
                    try:
                        await asyncio.sleep(0) #testing
                        text = await OCR(img_data) #OCR 
                        #print(text)
                    except RuntimeError as timeout_error: 
                        print(bcolors.FAIL, "OCR Error:",bcolors.ENDC,filename, timeout_error)
                        #os.execv(sys.executable, ['python3'] + sys.argv) #restarts script
                        #os._exit(0); #break point
                        continue            

                    
                    if words_in_string(word, text):
                        
                        if store_flagged == 'True':
                            filename = (str(message.created_at) + filename) # make filename more unique
                            if (len(filename) >= 100): filename = filename[(len(filename)-10):] # trim if filename too big
                            await asyncio.sleep(0) #testing
                            fileLocation = os.path.join('./images/flagged', filename)
                            with open(fileLocation, 'wb') as img:
                                img.write(img_data)
                                

                        print(bcolors.WARNING, "Keyword found in OCR reading! Deleting chat message.", bcolors.ENDC)
                        print (text)
                        await message.delete()
                        
                        
                    
                    await asyncio.sleep(0) #testing
        i = i+100
        print(f"{i} messages searched until now. last message was: {last_message}")
        
        save_to_file(last_message)
        


#WATCH FOR MESSAGES IN REAL TIME
class MyClient(discord.Client):
    async def on_ready(self):
        if history_deletion == 'True':
            await delete_history()    

        print(f'Logged on as {self.user}!')        


    async def on_message(self, message):
        
        if message.attachments:
            url = message.attachments[0].url
            img_data = requests.get(url).content
            filename = url.split('/')[-1]
            filename = filename.split('?', 1)[0]
            
            

            if filename.endswith(".png") or filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".webp"):
                filename = (str(message.created_at) + filename) # make filename more unique
                if (len(filename) >= 100): filename = filename[(len(filename)-10):] # trim if filename too big

                fileLocation = os.path.join('./images', filename)
            
                open(fileLocation, 'wb').write(img_data)            

                print (bcolors.OKCYAN,"Processing attachments!",bcolors.ENDC)
            
                text = pytesseract.image_to_string(fileLocation)
                print (bcolors.OKGREEN, "OCR readings:", bcolors.ENDC, text)
            
            
                if words_in_string(word, text):
                     await message.delete()
                     shutil.move( fileLocation,'./images/flagged')
                     print (bcolors.WARNING, "Keyword found in OCR reading! Deleting chat message.", bcolors.ENDC)
                     if store_flagged == 'False':
                         os.remove(fileLocation)
                else: os.remove(fileLocation)
            
            

        


client = MyClient(intents=intents)
client.run(token)



