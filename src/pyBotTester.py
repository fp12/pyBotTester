from config import appConfig
import discord
import asyncio

print('appStart')

clients = []

async def on_ready():
	print('client ready')

for b in appConfig['discord']:
	# create a new client
	c = discord.Client()
	# manually register its event (decorator won't work since it's in a list)
	setattr(c, 'on_ready', on_ready)
	clients.append(c)


loop = asyncio.get_event_loop()

try:
	startFuture = asyncio.gather(*(clients[i].start(appConfig['discord'][i]['token']) for i in range(len(clients))))
	loop.run_until_complete(startFuture)
except KeyboardInterrupt:
	logoutFuture = asyncio.gather(*(clients[i].logout() for i in range(len(clients))))
	loop.run_until_complete(logoutFuture)
finally:
    loop.close()

print('appStop')