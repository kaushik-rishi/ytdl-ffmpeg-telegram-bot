# YTDL FFMPEG MP3 TELEGRAM BOT

- input sanitization later, assume this format `<ytvid link> <start_time like mm:ss> <end_time mm:ss>`

## Architecture
- Maintain a `Jobs` table with the job id and status
- To handle failure, restarts, tracking where the job might be bailing/failing off
- Try thinking creating an architecture around queues
- Handle for more load
	- Learn how telegram (telebot) handles multiple requests
