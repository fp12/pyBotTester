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
    async def test_0_ping(self):
        defaultChannel = list(self._testBots[0].servers)[0].default_channel
        await self._testBots[0].send_message(defaultChannel, '>>> ping')
        result = await self._testBots[0].wait_for_message(timeout=2.0, channel=defaultChannel, author=self._bot)
        self.assertNotNone(result)
        self.assertStartsWith(result.content, '✅')

    async def test_1_username(self):
        defaultChannel = list(self._testBots[0].servers)[0].default_channel
        await self._testBots[0].send_message(defaultChannel, '>>> username')
        result = await self._testBots[0].wait_for_message(timeout=2.0, channel=defaultChannel, author=self._bot)
        self.assertNotNone(result)
        self.assertStartsWith(result.content, '❌') # missing parameters

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
        await self._testBots[1].send_message(self._bot, '>>> key qw' + _get_random_key())
        result2 = await self._testBots[1].wait_for_message(timeout=2.0, channel=privateChannel2, author=self._bot)
        self.assertNotNone(result2)
        self.assertStartsWith(result2.content, '❌') # bad api key format

        await self._testBots[1].send_message(self._bot, '>>> key ' + _get_random_key())
        result2 = await self._testBots[1].wait_for_message(timeout=2.0, channel=privateChannel2, author=self._bot)
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

class TestCase_Tournament_Simple(FeatureTest):
    def init(self):
        self.managementChannel = self._testBots[1].get_channel('188517631920308226')
        self.goodName = 'bot_' + _get_random_name()
        self.tourneyChannel = None

    async def setup(self):
        await self._testBots[1].send_message(self.managementChannel, '>>> create ' + self.goodName + ' ' + self.goodName + ' singleelim')
        result = await self._testBots[1].wait_for_message(timeout=5.0, channel=self.managementChannel, author=self._bot)
        self.assertNotNone(result)
        self.assertStartsWith(result.content, '✅')
        self.tourneyChannel = [c for c in list(self._testBots[1].servers)[0].channels if c.name == 't_' + self.goodName][0]
        self.assertNotNone(self.tourneyChannel)
        tourneyRole = [r for r in list(self._testBots[1].servers)[0].roles if r.name == 'Participant_' + self.goodName][0]
        self.assertNotNone(tourneyRole)

    async def test_1_join(self):
        # Bot 0, 1 & 2 join the tournament
        await self._testBots[0].send_message(self.tourneyChannel, '>>> join')
        result = await self._testBots[0].wait_for_message(timeout=5.0, channel=self.tourneyChannel, author=self._bot)
        self.assertNotNone(result)
        self.assertStartsWith(result.content, '✅')
        await self._testBots[1].send_message(self.tourneyChannel, '>>> join')
        result = await self._testBots[1].wait_for_message(timeout=5.0, channel=self.tourneyChannel, author=self._bot)
        self.assertNotNone(result)
        self.assertStartsWith(result.content, '✅')
        await self._testBots[2].send_message(self.tourneyChannel, '>>> join')
        result = await self._testBots[2].wait_for_message(timeout=5.0, channel=self.tourneyChannel, author=self._bot)
        self.assertNotNone(result)
        self.assertStartsWith(result.content, '✅')

    async def test_2_start(self):
        # Bot 1 starts the tournament
        await self._testBots[1].send_message(self.tourneyChannel, '>>> start')
        result = await self._testBots[1].wait_for_message(timeout=8.0, channel=self.tourneyChannel, author=self._bot)
        self.assertNotNone(result)
        self.assertStartsWith(result.content, '✅')

    async def test_3_score_update(self):
        # Bot 2 update his score against bot 1
        await self._testBots[2].send_message(self.tourneyChannel, '>>> update 123 bot')
        result = await self._testBots[2].wait_for_message(timeout=5.0, channel=self.tourneyChannel, author=self._bot)
        self.assertNotNone(result)
        self.assertStartsWith(result.content, '❌')  # wrong score format

        await self._testBots[2].send_message(self.tourneyChannel, '>>> update 1-23 bot')
        result = await self._testBots[2].wait_for_message(timeout=5.0, channel=self.tourneyChannel, author=self._bot)
        self.assertNotNone(result)
        self.assertStartsWith(result.content, '❌')  # wrong opponent name

        await self._testBots[2].send_message(self.tourneyChannel, '>>> update 1-23 ' + self._testBots[0].user.mention)
        result = await self._testBots[2].wait_for_message(timeout=5.0, channel=self.tourneyChannel, author=self._bot)
        self.assertNotNone(result)
        self.assertStartsWith(result.content, '❌')  # wrong opponent

        await self._testBots[2].send_message(self.tourneyChannel, '>>> update 1-23 ' + self._testBots[1].user.mention)
        result = await self._testBots[2].wait_for_message(timeout=5.0, channel=self.tourneyChannel, author=self._bot)
        self.assertNotNone(result)
        self.assertStartsWith(result.content, '✅')

        # Bot 1 update his score against bot 0
        await self._testBots[1].send_message(self.tourneyChannel, '>>> update 5-2,2-5,5-4 ' + self._testBots[0].user.mention)
        result = await self._testBots[1].wait_for_message(timeout=5.0, channel=self.tourneyChannel, author=self._bot)
        self.assertNotNone(result)
        self.assertStartsWith(result.content, '✅')

    async def test_4_finalize(self):
        # Bot 1 finalizes the tournament
        await self._testBots[1].send_message(self.tourneyChannel, '>>> finalize')
        result = await self._testBots[1].wait_for_message(timeout=5.0, channel=self.tourneyChannel, author=self._bot)
        self.assertNotNone(result)
        self.assertStartsWith(result.content, '✅')

        # Bot 2 can't write on the channel anymore
        await self.assertRaises(discord.Forbidden, self._testBots[2].send_message, destination=self.tourneyChannel, content='plop')

    async def teardown(self):
        await self._testBots[1].send_message(self.tourneyChannel, '>>> destroy')
        result = await self._testBots[1].wait_for_message(timeout=7.0, channel=self.managementChannel, author=self._bot)
        self.assertNotNone(result)
        self.assertStartsWith(result.content, '✅')
        self.tourneyChannel = [c for c in list(self._testBots[1].servers)[0].channels if c.name == 't_' + self.goodName]
        self.assertTrue(len(self.tourneyChannel) == 0)
        tourneyRole = [r for r in list(self._testBots[1].servers)[0].roles if r.name == 'Participant_' + self.goodName]
        self.assertTrue(len(tourneyRole) == 0)



