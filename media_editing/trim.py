import ffmpeg

# https://github.com/kkroening/ffmpeg-python/issues/184#issuecomment-504390452
def trim_audio(input_path, output_path, start=30, end=100):
    try:
        input_stream = ffmpeg.input(input_path)

        aud = (
            input_stream.audio
            .filter_('atrim', start=start, end=end)
            # .filter_('asetpts', 'PTS-STARTPTS')
        )

        # joined = ffmpeg.concat(vid, aud, v=1, a=1).node
        output = ffmpeg.output(aud, output_path)
        output.run()
        return True
    except Exception as e:
        print(e)
        return False

if __name__ == "__main__":
    trim_audio("./sobit.mp3", "newout.mp3")