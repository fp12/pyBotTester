# pyBotTester

A suite for running unit tests on your [Discord](https://discordapp.com/) bots


Setup:

Create the file config/config.json and fill it up with your information:
```json
{
  "discord":
  [
  	{
  		"name": "Tester Bot #1",
	    "token": "token1"
	},
	{
		"name": "Tester Bot #2",
		"token": "token2"
	}
  ]  
} 
```

You can add as many bots as you want



Dependencies:

[discord.py](https://github.com/Rapptz/discord.py)