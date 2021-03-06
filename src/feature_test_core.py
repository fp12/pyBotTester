import asyncio
import inspect
import time
import sys
import traceback
import re

class AssertionFailed(Exception):
    def __init__(self, text):
        self.text = text

    def __str__(self):
        return self.text


class FeatureEvent():
    def __init__(self):
        self.title = None
        self.info = None
        self.tb = None

    def __str__(self):
        if self.title == 'Success':
            return ''
        else:
            return self.title + ' ' + self.info + '\n' + self.tb

    def set_success(self):
        self.title = 'Success'
        return self
    
    def set_failure(self, exc):
        self.title = 'Failure'
        self.info = str(exc)
        self.tb = self._exc_info_to_string(exc)
        return self
    
    def set_error(self, exc):
        self.title = 'Error'
        self.info = str(exc)
        self.tb = self._exc_info_to_string(exc)
        return self

    def _exc_info_to_string(self, err):
        exctype, value, tb = sys.exc_info()
        tb = tb.tb_next 
        if exctype is AssertionFailed:
            return ''.join(traceback.format_exception(exctype, value, tb, 1)) 
        return ''.join(traceback.format_exception(exctype, value, tb)) 


class FeatureTester():
    async def start(self, bot, testbots):
        print('**** Feature Tests Starting ****')

        self._start_time = time.time()
        for fcls in FeatureTest.__subclasses__():
            events = []
            f = fcls(bot, testbots)
            
            try:
                await f.setup()
            except AssertionFailed as e:
                print('F', end='', flush=True)
                events.append(FeatureEvent().set_failure(e))
            except KeyboardInterrupt: 
                raise
            except Exception as e:
                print('E', end='', flush=True)
                evt = FeatureEvent()
                evt.set_error(e)
                events.append(evt)
            else:
                print('.', end='', flush=True)
                evt = FeatureEvent()
                evt.set_success()
                events.append(evt)

            for name, fct in inspect.getmembers(f, predicate=lambda x: inspect.ismethod(x) and x.__name__.startswith('test_')):
                try:
                    await fct()
                except AssertionFailed as e:
                    print('F', end='', flush=True)
                    events.append(FeatureEvent().set_failure(e))
                except KeyboardInterrupt: 
                    raise
                except Exception as e:
                    print('E', end='', flush=True)
                    evt = FeatureEvent()
                    evt.set_error(e)
                    events.append(evt)
                else:
                    print('.', end='', flush=True)
                    evt = FeatureEvent()
                    evt.set_success()
                    events.append(evt)
            
            try:
                await f.teardown()
            except AssertionFailed as e:
                print('F', end='', flush=True)
                events.append(FeatureEvent().set_failure(e))
            except KeyboardInterrupt: 
                raise
            except Exception as e:
                print('E', end='', flush=True)
                evt = FeatureEvent()
                evt.set_error(e)
                events.append(evt)
            else:
                print('.', end='', flush=True)
                evt = FeatureEvent()
                evt.set_success()
                events.append(evt)

            print('\n' + '\n'.join([str(e) for e in events if e.title != 'Success']))

        print ('**** Feature Tests Done ****')


featureTester = FeatureTester()


def get_var_name(var):
    stack = traceback.extract_stack()
    filename, lineno, function_name, code = stack[-3]
    vars_name = re.compile(r'\((.*?)\).*$').search(code).groups()[0]
    return vars_name

class FeatureTest():
    def __init__(self, bot, testbots):
        self._bot = bot
        self._testBots = testbots
        self.init()

    def init(self):
        pass

    async def setup(self):
        pass

    async def teardown(self):
        pass

    def fail(self, reason=''):
        raise AssertionFailed('fail: ' + reason)

    def assertNone(self, n):
        if n is not None:
            raise AssertionFailed('assertNone: {!r} is not None'.format(get_var_name(n)))

    def assertNotNone(self, n):
        if n is None:
            raise AssertionFailed('assertNotNone: {!r} is None'.format(get_var_name(n)))

    def assertTrue(self, cond):
        if not cond:
            raise AssertionFailed('assertTrue: {!r} is False'.format(cond))

    def assertIfNotEqual(self, c1, c2):
        if c1 != c2:
            raise AssertionFailed('assertIfNotEqual: \'{0!r}\' == \'{1!r}\''.format(c1, c2))

    def assertIfEqual(self, c1, c2):
        if c1 == c2:
            raise AssertionFailed('assertIfEqual: \'{0!r}\' != \'{1!r}\''.format(c1, c2))

    def assertStartsWith(self, str1, str2):
        if not str1.startswith(str2):
            raise AssertionFailed('assertStartsWith: \'{0!r}\' doesn\'t start with \'{1!r}\''.format(str1, str2))

    async def assertRaises(self, exc, func, **args):
        try:
            await func(**args)
        except exc:
            pass
        except Exception:
            raise
        else:
            raise AssertionFailed('assertRaises: \'{0!r}\' doesn\'t raise \'{1!r}\''.format(func.__name__, exc))


