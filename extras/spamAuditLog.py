from discord import SyncWebhook
import discord
import random
import string
intents = discord.Intents.default()
intents.message_content = True


def randomword(length):
   letters = ("abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ")
   return ''.join(random.choice(letters) for i in range(length))

async def on_message(self, message): 
        print(f'Message from {message.author}: {message.content}')


class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        channel = client.get_channel(YOUR CHANNEL ID) #int format
        while True:
                
            webhook = await channel.create_webhook(name=randomword(random.randint(5,10)))
            print('created')
            await asyncio.sleep(10)
            
            await webhook.delete()
            print("deleted")
            
client = MyClient(intents=intents)
client.run('YOUR BOT TOKEN')

