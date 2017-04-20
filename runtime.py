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
GOODMORNING_TEXT = settings['GOODMORNING_TEXT']
MOCK_DATA = '/Users/Tylerjeremy/Desktop/slack_ca/www/slack_ca/mock-data.json'

# instantiate Slack & Twilio clients
slack_client = SlackClient(settings['SLACK_BOT_TOKEN'])

def main():
    # Open the mock_data we have
    with open(MOCK_DATA) as data_file:
        # Load the mock-data as json
        data = json.load(data_file)
        # Loop over the data
        for marjorkey, subdict in data.items():
            total_entries = len(subdict)
            # Check if the majorkey is recognized so we calculate the
            # the average time for the majorkey.
            if marjorkey == 'agenda':
                total_time = 0
                for time in subdict:
                    parsed_time = time['time']
                    total_time += sum(x * int(t) for x, t in zip([3600, 60, 1],
                        parsed_time.split(":")))
                    avg_time_agenda = (total_time / 3600) / total_entries
            if marjorkey == 'start':
                total_time = 0
                for time in subdict:
                    parsed_time = time['time']
                    total_time += sum(x * int(t) for x, t in zip([3600, 60, 1],
                        parsed_time.split(":")))
                    avg_time_start = (total_time / 3600) / total_entries

        # Get the time for now in hours
        now_minutes = 0
        now_minutes += sum(x * int(t) for x, t in zip([3600, 60, 1],
            now_time.split(":")))
        now_hours = now_minutes / 3600
        # Uncomment this to show hours minutes and seconds format.
        # now_time = strftime("%H:%M:%S", localtime())

        # Check if the difference is low enough to send a message to the user.
        if -0.1 <= (avg_time_agenda - now_hours) <= 0.1:
            slack_client.api_call("chat.postMessage", channel=CHANNEL,
                                  text=AGENDA_TEXT, as_user=True)
            response = get_aqcuistion("agenda")
            slack_client.api_call("chat.postMessage", channel=CHANNEL,
                                  text=response, as_user=True)
        if -0.1 <= (avg_time_start - now_hours) <= 0.1:
            slack_client.api_call("chat.postMessage", channel=CHANNEL,
                                  text=GOODMORNING_TEXT, as_user=True)

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
