from feature_test_core import FeatureTest
import asyncio
import discord
import random
import string


def _get_random_name():
    return "".join(random.choice(string.ascii_lowercase) for _ in range(0, 15))


def _get_random_key():
    return "".join(random.choice(string.ascii_letters) for _ in range(0, 40))


def _get_random_name_too_long():
    return "".join(random.choice(string.ascii_letters) for _ in range(0, 70))
      


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

        managementChannel = self._testBots[1].get_channel('188517631920308226')
        await self._testBots[1].send_message(managementChannel, '>>> organization ' + _get_random_name())
        result2 = await self._testBots[1].wait_for_message(timeout=2.0, channel=managementChannel, author=self._bot)
        self.assertNotNone(result2)
        self.assertStartsWith(result2.content, '✅')

class TestCase_Tournament(FeatureTest):
    async def test_1_promotion_demotion(self):
        managementChannel = self._testBots[1].get_channel('188517631920308226')

        await self._testBots[1].send_message(managementChannel, '>>> promote')
        result = await self._testBots[1].wait_for_message(timeout=2.0, channel=managementChannel, author=self._bot)
        self.assertNotNone(result)
        self.assertStartsWith(result.content, '❌')  # not enough parameters

        await self._testBots[1].send_message(managementChannel, '>>> promote ' + self._testBots[2].user.mention)
        result = await self._testBots[1].wait_for_message(timeout=2.0, channel=managementChannel, author=self._bot)
        self.assertNotNone(result)
        self.assertStartsWith(result.content, '✅')

        await self._testBots[1].send_message(managementChannel, '>>> demote')
        result = await self._testBots[1].wait_for_message(timeout=2.0, channel=managementChannel, author=self._bot)
        self.assertNotNone(result)
        self.assertStartsWith(result.content, '❌')  # not enough parameters

        await self._testBots[1].send_message(managementChannel, '>>> demote ' + self._testBots[2].user.mention)
        result = await self._testBots[1].wait_for_message(timeout=2.0, channel=managementChannel, author=self._bot)
        self.assertNotNone(result)
        self.assertStartsWith(result.content, '✅')

    async def test_2_creation_destruction(self):
        managementChannel = self._testBots[1].get_channel('188517631920308226')
        await self._testBots[1].send_message(managementChannel, '>>> create')
        result = await self._testBots[1].wait_for_message(timeout=2.0, channel=managementChannel, author=self._bot)
        self.assertNotNone(result)
        self.assertStartsWith(result.content, '❌')  # not enough parameters

        await self._testBots[1].send_message(managementChannel, '>>> create ' + _get_random_name_too_long() + ' goodUrl swiss')
        result = await self._testBots[1].wait_for_message(timeout=5.0, channel=managementChannel, author=self._bot)
        self.assertNotNone(result)
        self.assertStartsWith(result.content, '❌')  # name too long

        await self._testBots[1].send_message(managementChannel, '>>> create ' + _get_random_name() + ' B@durl swiss')
        result = await self._testBots[1].wait_for_message(timeout=3.0, channel=managementChannel, author=self._bot)
        self.assertNotNone(result)
        self.assertStartsWith(result.content, '❌')  # bad url

        await self._testBots[1].send_message(managementChannel, '>>> create ' + _get_random_name() + ' ' + _get_random_name() + ' dbleelim')
        result = await self._testBots[1].wait_for_message(timeout=2.0, channel=managementChannel, author=self._bot)
        self.assertNotNone(result)
        self.assertStartsWith(result.content, '❌')  # bad type

        goodName = 'bot_' + _get_random_name()
        await self._testBots[1].send_message(managementChannel, '>>> create ' + goodName + ' ' + goodName + ' doubleelim')
        result = await self._testBots[1].wait_for_message(timeout=5.0, channel=managementChannel, author=self._bot)
        self.assertNotNone(result)
        self.assertStartsWith(result.content, '✅')
        tourneyChannel = [c for c in list(self._testBots[1].servers)[0].channels if c.name == 't_' + goodName][0]
        self.assertNotNone(tourneyChannel)
        tourneyRole = [r for r in list(self._testBots[1].servers)[0].roles if r.name == 'Participant_' + goodName][0]
        self.assertNotNone(tourneyRole)

        await self._testBots[1].send_message(managementChannel, '>>> destroy')
        result = await self._testBots[1].wait_for_message(timeout=5.0, channel=managementChannel, author=self._bot)
        self.assertNotNone(result)
        self.assertStartsWith(result.content, '❌')  # wrong channel

        await self._testBots[1].send_message(tourneyChannel, '>>> destroy')
        result = await self._testBots[1].wait_for_message(timeout=7.0, channel=managementChannel, author=self._bot)
        self.assertNotNone(result)
        self.assertStartsWith(result.content, '✅')
        tourneyChannel = [c for c in list(self._testBots[1].servers)[0].channels if c.name == 't_' + goodName]
        self.assertTrue(len(tourneyChannel) == 0)
        tourneyRole = [r for r in list(self._testBots[1].servers)[0].roles if r.name == 'Participant_' + goodName]
        self.assertTrue(len(tourneyRole) == 0)


    


