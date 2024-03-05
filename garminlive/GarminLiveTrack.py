
import logging
import os
import requests
import datetime
import json 
from pprint import pprint
## Construct a module wich takes a link and returns JSON from the Garmin LiveTrack API

class GarminLiveTrack:
    def __init__(self, link):
        
        self.link = link
        self.uuid = link.split('/token')[0].split('/session')[1]
        self.json = None
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        self.logger.info(f"Link: {self.link}")
        self.last = 0
        self.history = []

        # Get inital JSON
        #curl 'https://livetrack.garmin.com/services/session/f8edb905-472b-4e8f-b7eb-4e9ce9520197/trackpoints?requestTime=1709660807815' --compressed -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0' -H 'Accept: application/json, text/javascript, */*; q=0.01' -H 'Accept-Language: de,en-US;q=0.7,en;q=0.3' -H 'Accept-Encoding: gzip, deflate, br' -H 'X-Requested-With: XMLHttpRequest' -H 'Connection: keep-alive' -H 'Referer: https://livetrack.garmin.com/session/f8edb905-472b-4e8f-b7eb-4e9ce9520197/token/EA2ED1E8DE918951E2DBD376A6CE26' -H 'Cookie: CONSENTMGR=c1:0%7Cc2:0%7Cc3:0%7Cc4:0%7Cc5:0%7Cc6:0%7Cc7:0%7Cc8:0%7Cc9:0%7Cc10:0%7Cc11:0%7Cc12:0%7Cc13:0%7Cc14:0%7Cc15:0%7Cts:1704387484724%7Cconsent:false; utag_main=v_id:018cd567b9510013ae19b0c3f3f505050001b00d00bd0$_sn:1$_ss:0$_st:1704389215492$ses_id:1704387393873%3Bexp-session$_pn:2%3Bexp-session; __cflb=02DiuHqrGQn546rCmtxTwDePVPvdRG15eh3cSTi7nbz9J; TAsessionID=69448201-050e-424e-85b9-7d622042b1bc|NEW; notice_behavior=implied,eu; notice_preferences=0:; notice_gdpr_prefs=0:; notice_poptime=1619726400000; cmapi_gtm_bl=ga-ms-ua-ta-asp-bzi-sp-awct-cts-csm-img-flc-fls-mpm-mpr-m6d-tc-tdc; cmapi_cookie_privacy=permit 1 required' -H 'Sec-Fetch-Dest: empty' -H 'Sec-Fetch-Mode: cors' -H 'Sec-Fetch-Site: same-origin' -H 'Pragma: no-cache' -H 'Cache-Control: no-cache' -H 'TE: trailers'
        
        self.session = requests.Session()
        # enable cookies for the session as default
        r = self.session.get(self.link)
        self.logger.info(f"Session: {self.session.cookies}")
        self.cookies = self.session.cookies
        
        
        #self.session.headers.update({'Accept': 'application/json, text/javascript, */*; q=0.01', 'Accept-Language': 'de,en-US;q=0.7,en;q=0.3', 'Accept-Encoding': 'gzip, deflate, br', 'X-Requested-With': 'XMLHttpRequest', 'Connection': 'keep-alive', 'Referer': f'{self.link}/token/EA2ED1E8DE918951E2DBD376A6CE26', 'Cookie': 'CONSENTMGR=c1:0%7Cc2:0%7Cc3:0%7Cc4:0%7Cc5:0%7Cc6:0%7Cc7:0%7Cc8:0%7Cc9:0%7Cc10:0%7Cc11:0%7Cc12:0%7Cc13:0%7Cc14:0%7Cc15:0%7Cts:1704387484724%7Cconsent:false; utag_main=v_id:018cd567b9510013ae19b0c3f3f505050001b00d00bd0$_sn:1$_ss:0$_st:1704389215492$ses_id:1704387393873%3Bexp-session$_pn:2%3Bexp-session; __cflb=02DiuHqrGQn546rCmtxTwDePVPvdRG15eh3cSTi7nbz9J; TAsessionID=69448201-050e-424e-85b9-7d622042b1bc|NEW; notice_behavior=implied,eu; notice_preferences=0:; notice_gdpr_prefs=0:; notice_poptime=1619726400000; cmapi_gtm_bl=ga-ms-ua-ta-asp-bzi-sp-awct-cts-csm-img-flc-fls-mpm-mpr-m6d-tc-tdc; cmapi_cookie_privacy=permit 1 required', 'Sec-Fetch-Dest': 'empty', 'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Site': 'same-origin', 'Pragma': 'no-cache', 'Cache-Control': 'no-cache', 'TE': 'trailers'})
        #self.session.get(self.link + '/trackpoints?requestTime=' + str(int(datetime.datetime.now().timestamp() * 1000)))
        self.session.headers.update({'Referer': self.link})
        self.last = int(datetime.datetime.now().timestamp() * 1000)
        self.trackpoints = self.session.get('https://livetrack.garmin.com/services/session' + self.uuid + '/trackpoints').json()
        self.history.append(self.trackpoints['trackPoints'])
        


    def getTrackpoints(self, start=None, end=None):
        """
        Get the trackpoints for this activity.

        :param start: The start index for the trackpoints. If not provided, defaults to 0.
        :param end: The end index for the trackpoints. If not provided, defaults to the end of the trackpoints.
        :return: A list of trackpoints.
        """
        #if start is None:
        #    start = 0
        #if end is None:
        #    end = len(self.trackpoints)
        #return self.trackpoints[start:end]
        return self.trackpoints

    def update(self):
        """
        Update the trackpoints for this activity.
        """
        #self.trackpoints = self.session.get('https://livetrack.garmin.com/services/session' + self.link + '/trackpoints').json()
        self.session.headers.update({'Referer': self.link, 'TE': 'trailers'})
        print(self.session.headers)
        for name, value in self.session.cookies.items():
            print(f"Cookie: {name} = {value}")
        update = int(datetime.datetime.now().timestamp() * 1000)
        print('https://livetrack.garmin.com/services/session' + self.uuid + '/trackpoints?requestTime=' + str(update) + '&from=' + str(self.last))
        self.trackpoints = self.session.get('https://livetrack.garmin.com/services/session' + self.uuid + '/trackpoints?requestTime=' + str(update) + '&from=' + str(self.last)).json()
        self.last = update
        self.logger.info(f"Trackpoints: {self.trackpoints}")
        self.history.append(self.trackpoints['trackPoints'])
        return self.trackpoints
