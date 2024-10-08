from __future__ import annotations

from dataclasses import dataclass
from .const import STREET_ID_DICT, BASE_URL, DEFAULT_TIMEOUT
import aiohttp
import datetime
import logging

_LOGGER = logging.getLogger(__name__)

@dataclass
class BESTBottropGarbageCollectionDates:
    """ Class for managing connection and data to the BEST Bottrop garbage collection dates"""

    trash_types_json : list[dict] = ""
    session_timeout = aiohttp.ClientTimeout (total=None,sock_connect=DEFAULT_TIMEOUT,sock_read=DEFAULT_TIMEOUT)
    base_url = BASE_URL
    base_url_port = None

    def _get_name_for_id(self, x, json):
        for i in json:
            if i.get("id") == x:
                return i.get("name")
        return x

    def _today_or_later(self, x):
        # Check and return only if the date in the JSON is today or later
        xday, xmonth, xyear = x.get("formattedDate").split(".")
        xdate = datetime.date(int(xyear), int(xmonth), int(xday))

        if xdate >= datetime.datetime.today().date():
            return x;
        else: return "";

    def get_street_id_dict (self):
        return STREET_ID_DICT

    def get_id_for_name(self, x):
        return STREET_ID_DICT.get(x)

    async def get_trash_types (self):
        # Load the trashtypes
        # check if port was overwritten
        base_url : str = ""
        if self.base_url_port != None:
            base_url = self.base_url+":"+str(self.base_url_port)
        else:
            base_url = self.base_url

        try:
            async with aiohttp.ClientSession(timeout = self.session_timeout) as session:
                async with session.get(base_url+'/api/trashtype') as trash_types_response:
                    self.trash_types_json = await trash_types_response.json()
        except (aiohttp.ClientError, aiohttp.ClientConnectionError, TimeoutError) as e:
            _LOGGER.debug ("Could not load dates due to exception: %s", type(e).__name__)
            raise e

    async def get_dates_as_json(self, street_code, number) -> list[dict]:
        dates_json = ""
        # check if port was overwritten
        base_url : str = ""
        if self.base_url_port != None:
            base_url = self.base_url+":"+str(self.base_url_port)
        else:
            base_url = self.base_url

        if (street_code != None and self.trash_types_json != None):
            try:  
                async with aiohttp.ClientSession(timeout = self.session_timeout) as session:
                   async with session.get(base_url+'/api/street/{0}/house/{1}/collection'.format(street_code, number)) as dates:
                        dates_json = await dates.json()
                        dates_json = list(filter(self._today_or_later, dates_json))
            except (aiohttp.ClientError, aiohttp.ClientConnectionError, TimeoutError) as e:
                _LOGGER.debug ("Could not load dates due to exception: %s", type(e).__name__)
                raise e

            for date_item in dates_json:
                date_item.update({"trashType": self._get_name_for_id(date_item.get("trashType"), self.trash_types_json)})

        return dates_json
        