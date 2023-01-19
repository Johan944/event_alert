from datetime import datetime
import json
import pytz
import requests

try: 
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup

class ParserError(Exception):
    pass

class BadUrlError(Exception):
    pass

class Parser:
    def __init__(self):
        pass

    def get_offers(self):
        pass
class ParserShotgun(Parser):
    def __init__(self):
        super().__init__()

        self._keys_mapping = {"offers": "offers", "startDate": "utc_start", "endDate": "utc_end", "organizer": "organizer", "location": "location"}


    def get_infos(self, url):
        try:
            fp = requests.get(url)
        except:
            raise BadUrlError()
    
        html = fp.text
        parsed_html = BeautifulSoup(html, features="html.parser")
        scripts = parsed_html.findAll("script", type='application/ld+json')
        if parsed_html.findAll("h1"):
            name = parsed_html.findAll("h1")[0].text
        else:
            name = None

        infos = {"name": name, "utc_start": None, "utc_end": None}
        for python_key in self._keys_mapping.values():
            infos[python_key] = None

        for script in scripts:
            for content in script.contents:
                json_content = json.loads(content)

                for html_key, python_key in self._keys_mapping.items():
                    if html_key in json_content:
                        infos[python_key] = json_content[html_key]

        if infos["utc_start"] and infos["utc_end"]:
            infos["start"] = self._convert_date(infos["utc_start"], infos["location"]["address"]["addressCountry"])
            infos["end"] = self._convert_date(infos["utc_end"], infos["location"]["address"]["addressCountry"])

        return infos

    
    def _convert_date(self, date, country_code):
        timezone = pytz.country_timezones[country_code][0]
        local_tz = pytz.timezone(timezone)

        utc_dt = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ")
        local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)

        return local_tz.normalize(local_dt).strftime('%d-%m-%Y %H:%M')            
