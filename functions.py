import os
from inputs import *
def process_silence_report(report_file_path, min_silence_duration):
    
    report_file = open(report_file_path, 'r')
    chapter_starts = [0.5]
    for line in report_file.readlines():
        if line.startswith("[silencedetect"):
            words=line.split(" ")
            if len(words) != 8:
                continue
            silence_end, duration = words[4], words[7]
            if float(duration)>min_silence_duration:
                chapter_starts.append(float(silence_end))
    return chapter_starts

def generate_commands(audio_file = "", chapter_starts = [], preface_count=0):
    """
    generates the commands for splitting the <audio_file> into
    chapters based on <chapter_starts>
    chapter_starts --> list of chapter starting time in seconds
    """
    book_name = (audio_file.split("/")[-1]).split(".")[0]
    audio_dir_path = audio_file[:audio_file.rindex("/")]
    chapters_dir_path = f"{audio_dir_path}/{book_name}"
    start = chapter_starts[0]
    commands = [rf"mkdir '{chapters_dir_path}'"]
    ch = -preface_count + 1
    for i in range(1,len(chapter_starts)):
        end = chapter_starts[i]
        chapter_name = "Chapter " + str(ch)
        split_start = start - 1
        split_end = end + 2
        commands.append(f"ffmpeg -ss {split_start} -i '{audio_file}' -t {split_end} '{chapters_dir_path}/{chapter_name}.mp3'")
        start = end
        ch += 1
    commands.append(f"ffmpeg -ss {split_start-1} -i '{audio_file}' '{chapters_dir_path}/{'Chapter ' + str(ch)}.mp3'")
    return commands

def execute_commands(commands):
    """
    executes the list of commands supplied to it
    """
    for command in commands:
        os.system(command)

def split_audiobook_into_chapters(min_silence_duration, report_file_path, audio_file):
    chapter_starts = process_silence_report(report_file_path, min_silence_duration)
    commands = generate_commands(audio_file, chapter_starts, preface_count)
    execute_commands(commands)
    print(*commands, sep="\n")
    print("========successfully created chapters======")

split_audiobook_into_chapters(min_silence_duration, report_file_path, audio_file)

