
import json
import os
import subprocess


#STT
def STT(AUDIO_FILENAME):

    command=f"whisper {AUDIO_FILENAME}  --model medium --language en --device cuda --word_timestamps True"
    data= subprocess.Popen(command, stdout=subprocess.PIPE, shell=True).stdout.readlines()


    output_json=AUDIO_FILENAME.split('/')[-1].split('.')[0]+".json"
    files=os.listdir(os.getcwd())
    if output_json in files:
        with open(output_json, "r") as f:
            result=json.load(f)

    word_ts_hyp={AUDIO_FILENAME.split('/')[-1].split('.')[0]:[]}
    word_hyp={AUDIO_FILENAME.split('/')[-1].split('.')[0]:[]}

    for item in result['segments']:
        for stamp in item['words']:
            word_ts_hyp[AUDIO_FILENAME.split('/')[-1].split('.')[0]].append([stamp['start'], stamp['end']])

    for item in result['segments']:
        for stamp in item['words']:
            word_hyp[AUDIO_FILENAME.split('/')[-1].split('.')[0]].append(stamp['word'])

    if os.path.exists(AUDIO_FILENAME.split('/')[-1].split('.')[0]+".tsv"):
        os.remove(AUDIO_FILENAME.split('/')[-1].split('.')[0]+".tsv")
    if os.path.exists(AUDIO_FILENAME.split('/')[-1].split('.')[0]+".srt"):
        os.remove(AUDIO_FILENAME.split('/')[-1].split('.')[0]+".srt")
    if os.path.exists(AUDIO_FILENAME.split('/')[-1].split('.')[0]+".txt"):
        os.remove(AUDIO_FILENAME.split('/')[-1].split('.')[0]+".txt")
    if os.path.exists(AUDIO_FILENAME.split('/')[-1].split('.')[0]+".vtt"):
        os.remove(AUDIO_FILENAME.split('/')[-1].split('.')[0]+".vtt")
    if os.path.exists(AUDIO_FILENAME.split('/')[-1].split('.')[0]+".json"):
        os.remove(AUDIO_FILENAME.split('/')[-1].split('.')[0]+".json")

    return word_hyp, word_ts_hyp