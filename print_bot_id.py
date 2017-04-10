import os
from slackclient import SlackClient

# Insert BOT_NAME here to find it
BOT_NAME = 'ca'

# Use in terminal: export SLACK_BOT_TOKEN='{token}' to set this variable
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))

# Calling to find the ID of the bot, the terminal will log what it found.
if __name__ == "__main__":
    api_call = slack_client.api_call("users.list")
    if api_call.get('ok'):
        # retrieve all users so we can find our bot
        users = api_call.get('members')
        for user in users:
            if 'name' in user and user.get('name') == BOT_NAME:
                print("Bot ID for '" + user['name'] + "' is " + user.get('id'))
    else:
        print("could not find bot user with the name " + BOT_NAME)
