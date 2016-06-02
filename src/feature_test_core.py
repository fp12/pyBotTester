import asyncio
import inspect
import time


class AssertionFailed(Exception):
    def __init__(self, text):
        self.text = text

    def __str__(self):
        return self.text


class FeatureTester():
    async def start(self, bot, testbots):
        print('**** Feature Tests Starting ****')

        self._start_time = time.time()
        for fcls in FeatureTest.__subclasses__():
            failures = []
            errors = []
            f = fcls(bot, testbots)
            await f.setup()
            for name, fct in inspect.getmembers(f, predicate=lambda x: inspect.ismethod(x) and x.__name__.startswith('test_')):
                try:
                    await fct()
                except AssertionFailed as e:
                    failures.append(e)
                except Exception as e:
                    errors.append(e)

                if len(errors) > 0:
                    print('E', end='')
                elif len(failures) > 0:
                    print('F', end='')
                else:
                    print('.', end='')
            await f.teardown()

            print()
            if len(errors) > 0:
                print('\n'.join([str(e) for e in errors]))
            elif len(failures) > 0:
                print('\n'.join([str(e) for e in failures]))

        print ('**** Feature Tests Done ****')


featureTester = FeatureTester()


class FeatureTest():
    def __init__(self, bot, testbots):
        self._bot = bot
        self._testBots = testbots

    async def setup(self):
        pass

    async def teardown(self):
        pass

    def fail(self, reason=''):
        raise AssertionFailed('fail ' + reason)

    def assertNotNone(self, n):
        if n is None:
            raise AssertionFailed('assertNotNone')

    def assertTrue(self, cond):
        if not cond:
            raise AssertionFailed('assertTrue')

    def assertIfNotEqual(self, c1, c2):
        if c1 != c2:
            raise AssertionFailed('assertIfNotEqual')

    def assertIfEqual(self, c1, c2):
        if c1 == c2:
            raise AssertionFailed('assertIfEqual')
