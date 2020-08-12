import requests
import schedule
import time
import pandas as pd
import random

# Set token
TOKEN = ''
# Set CSV
CSV = ''
# chat ID
CHAT_ID = ''
# recently posted news
previousMessage = []

#Send message to group and return JSON response
def send_message(message, botToken, chatId):
    url = 'https://api.telegram.org/bot{}/sendMessage?chat_id={}&parse_mode=Markdown&text={}'.format(botToken, chatId, message)
    response = requests.get(url)
    return response.json()


def import_csv(csv):
    df = pd.read_csv(csv, names=['message'])
    return df


def job():
    
    #get messages
    messages = import_csv(CSV)

    #recycle news after half the set
    if len(previousMessage) > len(messages)/2 : previousMessage.pop()

    #pick new message if not in previous message set
    while True:
        randomPick = random.randint(0,len(messages)-1)
        if randomPick not in previousMessage:
            previousMessage.insert(0, randomPick)
            break
    send_message(messages.message[randomPick], TOKEN, CHAT_ID)


job()

#Create schedule to run every two hours
schedule.every(2).hours.do(job)

#keep programming running to trigger schedule
while True:
    schedule.run_pending()
    time.sleep(1)

