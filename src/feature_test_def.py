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
    async def test_username(self):
        defaultChannel = list(self._testBots[0].servers)[0].default_channel
        privateChannel = await self._testBots[0].start_private_message(self._bot)
        await self._testBots[0].send_message(defaultChannel, '>>> username Bot1' + _get_random_name())
        result = await self._testBots[0].wait_for_message(timeout=2.0, channel=privateChannel, author=self._bot)
        self.assertNotNone(result)

    async def test_key(self):
        privateChannel = await self._testBots[0].start_private_message(self._bot)
        await self._testBots[0].send_message(privateChannel, '>>> key ' + _get_random_key())
        result = await self._testBots[0].wait_for_message(timeout=2.0, channel=privateChannel, author=self._bot)
        self.assertNotNone(result)
        self.assertNotTrue(result.starts_with('Error'))
