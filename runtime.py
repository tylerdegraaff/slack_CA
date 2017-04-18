import os
import time
import json
import datetime
import math

from time import strftime, localtime
from pprint import pprint
from slackclient import SlackClient
from settings import settings
from slack_ca.factories.external_factory import get_aqcuistion

# starterbot's ID as an environment variable
BOT_ID = settings['BOT_ID']

# constants
AT_BOT = "<@" + BOT_ID + ">"
CHANNEL = settings['CHANNEL']
AGENDA_TEXT = settings['PREDICT_AGENDA_TEXT']

# instantiate Slack & Twilio clients
slack_client = SlackClient(settings['SLACK_BOT_TOKEN'])

def main():
    with open('mock-data.json') as data_file:
        data = json.load(data_file)
        total_time = 0

        for marjorkey, subdict in data.items():
            print(marjorkey)
            total_entries = len(subdict)
            for time in subdict:
                parsed_time = time['time']
                total_time += sum(x * int(t) for x, t in zip([3600, 60, 1],
                    parsed_time.split(":")))

        avg_time = (total_time / 3600) / total_entries
        now_minutes = 0
        now_time = strftime("%H:%M:%S", localtime())
        now_minutes += sum(x * int(t) for x, t in zip([3600, 60, 1],
            now_time.split(":")))
        now_hours = now_minutes / 3600

        if (avg_time - now_hours) <= 0.3:
            slack_client.api_call("chat.postMessage", channel=CHANNEL,
                                  text=AGENDA_TEXT, as_user=True)
            response = get_aqcuistion("agenda")
            slack_client.api_call("chat.postMessage", channel=CHANNEL,
                                  text=response, as_user=True)
            return

        return

if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print('Running runtime script')
        while True:
            main()
            break
    else:
        print('Connection failed')
