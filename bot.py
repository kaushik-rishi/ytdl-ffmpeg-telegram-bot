# ref later
# https://github.com/python-telegram-bot/python-telegram-bot/issues/1264#issuecomment-431400273

import telebot
from uuid import uuid4
from dotenv import load_dotenv
import os
import re
from downloaders import download_audio
from media_editing import trim_audio
import requests

load_dotenv()

# move to utils


def get_seconds_from_timestamp(timestamp):
    minutes, seconds = timestamp.split(":")
    total_seconds = int(minutes) * 60 + int(seconds)
    return total_seconds


# Set up the bot
bot = telebot.TeleBot(os.getenv("BOT_TOKEN"))


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(chat_id=message.chat.id,
                     text="Hi, I'm an echo bot. Send me a message and I'll echo it back!")


@bot.message_handler(commands=['audio'])
def audio(message):
    try:
        # Split the message into its components
        message_parts = message.text.split()
        youtube_video_link = message_parts[1]
        start_timestamp = message_parts[2]
        end_timestamp = message_parts[3]

        start_seconds = get_seconds_from_timestamp(start_timestamp)
        end_seconds = get_seconds_from_timestamp(end_timestamp)

        print(start_seconds, end_seconds, youtube_video_link, end="\n")

        # Send a response
        bot.send_message(chat_id=message.chat.id,
                         text="Started proccessing")

        print("start: audio download")
        id = str(uuid4())
        status, file_name = download_audio(youtube_video_link, id)
        print(status, file_name)
        if status:
            print("success video download")
        print("end: audio download")

        print("start: audio trim")
        trimmed_file_path = f"trimmed_bucket/{id}.mp3"
        status = trim_audio(file_name, trimmed_file_path,
                            start=start_seconds, end=end_seconds)
        print("audio trim status: ", status)
        if status:
            print("success audio trim")
        print("end: audio trim")

        doc = open(trimmed_file_path, 'rb')
        print(doc)
        bot.send_document(message.from_user.id, doc, timeout=200)

        # Send a response
        bot.send_message(chat_id=message.chat.id,
                         text="Finished proccessing")

        print("finished!!")

    except Exception as e:
        # Send an error message if there was an error parsing the message
        bot.send_message(chat_id=message.chat.id, text="Error: " + str(e))


@bot.message_handler(commands=['reel'])
def reel(message):
    try:
        # Split the message into its components
        message_parts = message.text.split()
        reel_url = message_parts[1]
        shortcode = re.search(r'/reel/(\w+)/?', reel_url).group(1)

        headers = {
            'X-RapidAPI-Host': 'instagram-bulk-profile-scrapper.p.rapidapi.com',
            'X-RapidAPI-Key': '566a1a3b45mshf8dae33e2558c9dp1fcc0bjsn474b63726369',
        }

        params = {
            'shortcode': shortcode,
            'response_type': 'reels',
        }

        response = requests.get(
            'https://instagram-bulk-profile-scrapper.p.rapidapi.com/clients/api/ig/media_by_id',
            params=params,
            headers=headers,
        )
        data = response.json()
        reel_media_url = data[0]['items'][0]['video_versions'][0]['url']
        print(reel_media_url)

        # Send a response
        bot.send_message(chat_id=message.chat.id,
                         text=reel_media_url)

    except Exception as e:
        # Send an error message if there was an error parsing the message
        bot.send_message(chat_id=message.chat.id, text="Error: " + str(e))


# Start the bot
print("started the bot")
bot.polling()
