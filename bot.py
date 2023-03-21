import telebot
from uuid import uuid4
from dotenv import load_dotenv
import os
from downloaders import download_audio
from media_editing import trim_audio

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
        bot.send_document(message.from_user.id, doc, timeout=100)

        # Send a response
        bot.send_message(chat_id=message.chat.id,
                         text="Finished proccessing")

        print("finished!!")

    except Exception as e:
        # Send an error message if there was an error parsing the message
        bot.send_message(chat_id=message.chat.id, text="Error: " + str(e))


# Start the bot
print("started the bot")
bot.polling()
