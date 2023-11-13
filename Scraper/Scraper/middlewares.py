# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from urllib.parse import urlencode
from random import randint
from scrapy import Request
import requests

class ScrapeOps_Fake_User_Agent_Middleware:

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)
    
    def __init__(self,settings):
        self.scrapeops_api_key = settings.get("SCRAPEOPS_API_KEY")
        self.scrapeops_endpoint = settings.get("SCRAPEOPS_FAKE_USER_AGENT_ENDPOINT", "https://headers.scrapeops.io/v1/user-agents?")
        self.scrapeops_fake_user_agents_active = settings.get("SCRAPEOPS_FAKE_USER_AGENT_ENABLED", False)
        self.scrapeops_num_results = settings.get("SCRAPEOPS_NUM_RESULTS")
        self.headers_list = []
        self._get_user_agents_list()
        self._scrapeops_fake_user_agents_enabled()

    def _get_user_agents_list(self):
        payload = {"api_key": self.scrapeops_api_key}
        if self.scrapeops_num_results is not None:
            payload["num_results"] = self.scrapeops_num_results
        response = requests.get(self.scrapeops_endpoint, params=urlencode(payload))
        json_response = response.json()
        self.user_agents_list = json_response.get("result", [])

    def _get_random_user_agent(self):
        random_index = randint(0, len(self.user_agents_list) - 1)
        return self.user_agents_list[random_index]
    
    def _scrapeops_fake_user_agents_enabled(self):
        if self.scrapeops_api_key is None or self.scrapeops_api_key == "" or self.scrapeops_fake_user_agents_active == False:
            self.scrapeops_fake_user_agents_active = False
        else:
            self.scrapeops_fake_user_agents_active = True

    def process_request(self, request, spider):
        random_user_agent = self._get_random_user_agent()
        request.headers["User-Agent"] = random_user_agent

        print("************ NEW HEADER ATTACHED *******")
        print(request.headers['User-Agent'])

class ScrapeOps_Fake_Browser_Header_Agent_Middleware:

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def __init__(self, settings):
        self.scrapeops_api_key = settings.get('SCRAPEOPS_API_KEY')
        self.scrapeops_endpoint = settings.get('SCRAPEOPS_FAKE_BROWSER_HEADER_ENDPOINT', 'http://headers.scrapeops.io/v1/browser-headers') 
        self.scrapeops_fake_browser_headers_active = settings.get('SCRAPEOPS_FAKE_BROWSER_HEADER_ENABLED', True)
        self.scrapeops_num_results = settings.get('SCRAPEOPS_NUM_RESULTS')
        self.headers_list = []
        self._get_headers_list()
        self._scrapeops_fake_browser_headers_enabled()

    def _get_headers_list(self):
        payload = {'api_key': self.scrapeops_api_key}
        if self.scrapeops_num_results is not None:
            payload['num_results'] = self.scrapeops_num_results
        response = requests.get(self.scrapeops_endpoint, params=urlencode(payload))
        json_response = response.json()
        self.headers_list = json_response.get('result', [])

    def _get_random_browser_header(self):
        random_index = randint(0, len(self.headers_list) - 1)
        return self.headers_list[random_index]

    def _scrapeops_fake_browser_headers_enabled(self):
        if self.scrapeops_api_key is None or self.scrapeops_api_key == '' or self.scrapeops_fake_browser_headers_active == False:
            self.scrapeops_fake_browser_headers_active = False
        else:
            self.scrapeops_fake_browser_headers_active = True
    
    def process_request(self, request, spider):        
        random_browser_header = self._get_random_browser_header()

        request.headers['accept-language'] = random_browser_header['accept-language']
        request.headers['sec-fetch-user'] = random_browser_header['sec-fetch-user'] 
        request.headers['sec-fetch-mod'] = random_browser_header['sec-fetch-mod'] 
        request.headers['sec-fetch-site'] = random_browser_header['sec-fetch-site'] 
        request.headers['sec-ch-ua-platform'] = random_browser_header['sec-ch-ua-platform'] 
        request.headers['sec-ch-ua-mobile'] = random_browser_header['sec-ch-ua-mobile'] 
        request.headers['sec-ch-ua'] = random_browser_header['sec-ch-ua'] 
        request.headers['accept'] = random_browser_header['accept'] 
        request.headers['user-agent'] = random_browser_header['user-agent'] 
        request.headers['upgrade-insecure-requests'] = random_browser_header.get('upgrade-insecure-requests')
    
        print("************ NEW HEADER ATTACHED *******")
        print(request.headers)
