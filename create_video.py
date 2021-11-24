import ffmpeg
import argparse
import os

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--mp3", help="path to mp3 sound file", required=True)

    args = parser.parse_args()
    input_video = ffmpeg.input("project.mp4")
    input_audio = ffmpeg.input(args.mp3)
    if os.path.exists("finished_video.mp4"):
        os.remove("finished_video.mp4")
    ffmpeg.concat(input_video, input_audio, v=1, a=1).output('finished_video.mp4').run()
