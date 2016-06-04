from feature_test_core import FeatureTest
import asyncio
import discord
import random
import string


def _get_random_name():
    return "".join(random.choice(string.ascii_letters) for _ in range(0, 15))


def _get_random_key():
    return "".join(random.choice(string.ascii_letters) for _ in range(0, 40))


class TestCase_Settings(FeatureTest):
    async def test_1_username(self):
        defaultChannel = list(self._testBots[0].servers)[0].default_channel
        await self._testBots[0].send_message(defaultChannel, '>>> username Bot1' + _get_random_name())
        result1 = await self._testBots[0].wait_for_message(timeout=2.0, channel=defaultChannel, author=self._bot)
        self.assertNotNone(result1)
        self.assertStartsWith(result1.content, '✅')

        privateChannel = await self._testBots[0].start_private_message(self._bot)
        self.assertNotNone(privateChannel)
        await self._testBots[0].send_message(self._bot, '>>> username Bot1' + _get_random_name())
        result2 = await self._testBots[0].wait_for_message(timeout=2.0, channel=privateChannel, author=self._bot)
        self.assertNotNone(result2)
        self.assertStartsWith(result2.content, '✅')

    async def test_2_key(self):
        privateChannel1 = await self._testBots[0].start_private_message(self._bot)
        await self._testBots[0].send_message(self._bot, '>>> key ' + _get_random_key())
        result1 = await self._testBots[0].wait_for_message(timeout=2.0, channel=privateChannel1, author=self._bot)
        self.assertNotNone(result1)
        self.assertStartsWith(result1.content, '❌') # not enough privileges

        privateChannel2 = await self._testBots[1].start_private_message(self._bot)
        await self._testBots[1].send_message(self._bot, '>>> key ' + _get_random_key())
        result2 = await self._testBots[1].wait_for_message(timeout=2.0, channel=privateChannel2, author=self._bot)
        self.assertNotNone(result2)
        self.assertStartsWith(result2.content, '✅')

    async def test_3_organization(self):
        privateChannel1 = await self._testBots[0].start_private_message(self._bot)
        await self._testBots[0].send_message(self._bot, '>>> organization ' + _get_random_name())
        result1 = await self._testBots[0].wait_for_message(timeout=2.0, channel=privateChannel1, author=self._bot)
        self.assertNotNone(result1)
        self.assertStartsWith(result1.content, '❌') # not enough privileges

        privateChannel2 = await self._testBots[1].start_private_message(self._bot)
        await self._testBots[1].send_message(self._bot, '>>> organization ' + _get_random_name())
        result2 = await self._testBots[1].wait_for_message(timeout=2.0, channel=privateChannel2, author=self._bot)
        self.assertNotNone(result2)
        self.assertStartsWith(result2.content, '❌') # enough privileges but wrong channel

class TestCase_Tournament(FeatureTest):
    async def test_1_creation_destruction(self):
        newServer = await self._testBots[1].create(_get_random_name(), discord.ServerRegion.us_east)
        assertNotNone(newServer)
        