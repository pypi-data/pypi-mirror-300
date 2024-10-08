"""Basic tests for the BEST Bottrop API"""
import logging
import pytest
import aiohttp
from asyncio.proactor_events import _ProactorBasePipeTransport
from functools import wraps
import sys
import asyncio
from aiohttp import web
from unittest.mock import patch

LOGGER = logging.getLogger(__name__)
sys.path.append ("../src")
run_sleep : bool = False

from best_bottrop_garbage_collection_dates import BESTBottropGarbageCollectionDates

@pytest.mark.asyncio
async def test_load_trash_types():
    LOGGER.info ("test_load_trash_types")
    test_class = BESTBottropGarbageCollectionDates()
    print (test_class)
    try:
        await test_class.get_trash_types()
    except aiohttp.ClientError as e:
        LOGGER.error ("Could not load dates! Exception: {0}".format(e))
    assert test_class.trash_types_json != ""

@pytest.mark.asyncio
async def test_load_trash_types_and_check_content():
    LOGGER.info ("test_load_trash_types")
    garbage_type_str = ""
    test_class = BESTBottropGarbageCollectionDates()
    try:
        await test_class.get_trash_types()
    except aiohttp.ClientError as e:
        LOGGER.error ("Could not load dates! Exception: {0}".format(e))
    if ( test_class.trash_types_json != None and test_class.trash_types_json != "" ):
        test_class.trash_types_json[0].get("DFF3C375")
        for i in test_class.trash_types_json: 
            if i.get("id") == "DFF3C375":
                garbage_type_str = i.get("name")
    assert garbage_type_str == "Papiertonne"

@pytest.mark.asyncio
async def test_load_dates_pass():
    LOGGER.info("test_load_dates")
    l = None
    try:
        test_class = BESTBottropGarbageCollectionDates()
        street_code = test_class.get_id_for_name("Ernst-Wilczok-Platz")
        l = await test_class.get_dates_as_json(street_code, 1)
    except aiohttp.ClientError as e:
        LOGGER.error ("Could not load dates! Exception: {0}".format(e))
    assert (l != None and type(l) is list)

async def slow_handler(request):
    global run_sleep
    while (run_sleep):
        await asyncio.sleep(1)  # Simulating a long response until interrupted
    return web.Response(text="Slow response")

@pytest.fixture
def app():
    app = web.Application()
    return app

@pytest.mark.asyncio
async def test_load_dates_network_fail(mocker, app):
    LOGGER.info("test_load_dates_network_fail")

    test_timeout: int = 1

    # Patch the add_get method to use the slow_handler
    mocker.patch.object(app.router, 'add_get', side_effect=lambda path, handler: app.router.add_route('GET', path, slow_handler))
    app.router.add_get('/api/street/{street_id}/house/{house_id}/collection', slow_handler)
    
    # Start test server
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, 'localhost', 8080)
    await site.start()

    mocker.patch('aiohttp.web.Application', app())
    global run_sleep
    run_sleep = True
    
    try:
        test_class = BESTBottropGarbageCollectionDates()
        # reroute the request to the fake service to generate a time out
        mocker.patch.object(test_class, 'base_url', 'http://localhost')
        mocker.patch.object(test_class, 'base_url_port', '8080')
        # in order to shorten the test time, reduce the timeout to 1 second
        mocker.patch.object(test_class, 'session_timeout', aiohttp.ClientTimeout (total=None,sock_connect=test_timeout,sock_read=test_timeout))
        l = await test_class.get_dates_as_json("EEEB657D", 4)
        # Stop the test server
        await runner.cleanup()
        assert False
    except (aiohttp.ClientError, aiohttp.ClientConnectionError, TimeoutError) as e:
        LOGGER.info(e, exc_info = False)
        # Stop the test server
        run_sleep = False
        await runner.cleanup()
        assert type(e) == aiohttp.client_exceptions.SocketTimeoutError


@pytest.mark.asyncio
async def test_load_dates_fail():
    LOGGER.info("test_load_dates_fail")
    l = None
    try:
        test_class = BESTBottropGarbageCollectionDates()
        l = await test_class.get_dates_as_json("bla",200)
    except aiohttp.ClientError as e:
        LOGGER.info(e, exc_info = False)
    assert (l != None and [] == l)

def test_get_street_ids():
    test_class = BESTBottropGarbageCollectionDates()
    street_dict = test_class.get_street_id_dict()
    print (street_dict)
    assert (type(street_dict) is dict)

def silence_event_loop_closed(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except RuntimeError as e:
            if str(e) != 'Event loop is closed':
                raise
    return wrapper

# Silence the exception here.
_ProactorBasePipeTransport.__del__ = silence_event_loop_closed(_ProactorBasePipeTransport.__del__)
