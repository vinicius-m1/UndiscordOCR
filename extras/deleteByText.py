import discord
import pickle
from configparser import ConfigParser
import asyncio
import os.path
intents = discord.Intents.default()
intents.message_content = True

config = ConfigParser()
config.read("config.ini")
config_data = config['default']
token = config_data['token']
channel_id = int(config_data['channel_id'])
history_deletion = config_data['history_deletion']
server_id = int(config_data['server_id'])
word = config_data['word']
word = word.split(",")



def words_in_string(word_list, text):
    return set(word_list).intersection(text.split())

def save_to_file(variable):

    
    with open("last_message.pickle", 'wb') as handle:
        pickle.dump(variable,handle, protocol=pickle.HIGHEST_PROTOCOL)

def load_from_file():
    with open('last_message.pickle', 'rb') as handle:
         return(pickle.load(handle))

def get_channel_id(position):
    guild = client.get_guild(server_id)
    i =0
    for channel in guild.channels:
        if (type(channel) == discord.channel.TextChannel):
            i=i+1
            if (i == position):
                print (f"Selected Channel: {channel.name} - CH num: {i}")
                save_to_file(None)
                return(channel)
                
            #print (type(channel))    


async def delete_history():



    if not os.path.isfile('last_message.pickle'):
        print ("Creating save file for last message.")
        open('last_message.pickle', 'a').close()
        save_to_file(None)
    
    print (f"BLOCKED WORDS: {word}")

    

    i =0
    found = 0
    num_channels=0
    done_channels=0
    #last_message = None
    #save_to_file(last_message)
    
    guild = client.get_guild(server_id)
    for channel in guild.channels:
        if (type(channel) == discord.channel.TextChannel):
            num_channels=num_channels+1

    while (num_channels != done_channels): 
        done_channels = done_channels+1

        #if done_channels == 2:
            #done_channels = done_channels+1
        print (f"Channels: {done_channels}/{num_channels}")
        channel = get_channel_id(done_channels)

        async for message in channel.history(limit=1, oldest_first=True):
            first_message = message.created_at
        print ("first message: ",first_message) #getting where to stop searching for more messages


        while True:
            last_message = load_from_file();
            async for message in channel.history(limit = 100, before=last_message):
        
            
                last_message = message.created_at
                await asyncio.sleep(0) #testing
                #print (message.content)
                if words_in_string(word, message.content):
                            await asyncio.sleep(0) #testing
                            found = found+1
                            print("Keyword found! Deleting chat message.")
                            print (message.content)
                            await message.delete()
                            await asyncio.sleep(2)

    
                    
        
            print(f"{i} messages searched until now. last message was: {last_message} found: {found}")
            save_to_file(last_message)
            if (last_message == first_message or last_message == None): #last_message == None if there are no messages in chat
                print("Going to next channel")
                break;
            
            await asyncio.sleep(0) #testing
            i = i+100
    print ("Finished searching in all channels!")


class MyClient(discord.Client):

    async def on_ready(self):
        await delete_history()    

             


    async def on_message(self, message):
        print (message.content)
            

client = MyClient(intents=intents)
client.run(token)



