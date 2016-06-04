from config import appConfig
import discord
import asyncio
import unittest
import inspect
import feature_test_def
from feature_test_core import featureTester

print('appStart')

clients = []
ready = [0]


async def on_ready():
    ready[0] += 1
    print('{0} client(s) ready'.format(ready[0]))

async def on_message(message):
    if message.author.id == '150316380992962562' and message.content.startswith('start'):
        await featureTester.start(bot, clients)


for b in appConfig['discord']:
    # create a new client
    c = discord.Client()
    # manually register its event (decorator won't work since it's in a list)
    setattr(c, 'on_ready', on_ready)
    clients.append(c)

assert(len(clients) > 0)

async def unit_test_loop():
    while True:
        if ready[0] == len(clients):
            bot = discord.utils.get(clients[0].get_all_members(), id=appConfig['bot'])
            await featureTester.start(bot, clients)
            for c in clients:
                await c.logout()
            return
        else:
            await asyncio.sleep(2)

# manually register the on_message event
setattr(clients[0], 'on_message', on_message)

loop = asyncio.get_event_loop()

try:
    tasks = [clients[i].start(appConfig['discord'][i]['token'])
             for i in range(len(clients))]
    tasks.append(unit_test_loop())
    loop.run_until_complete(asyncio.gather(*tasks))
except (KeyboardInterrupt, SystemExit):
    logoutFuture = asyncio.gather(
        *(clients[i].logout() for i in range(len(clients))))
    loop.run_until_complete(logoutFuture)
finally:
    loop.close()

print('appStop')
