#independent
import os
import time
import uuid
import datetime
import torch
import gc
import shutil

import warnings
warnings.simplefilter("ignore")

#dependent
from audio_processing import AUDIO_DOWNLOAD
from stt import STT
from diarization import DIARIZATION
from speaker_matching import SPEAKER_MATCHING

#DIRECTORY CLEAN
def clean_directory(directory_path):

    """
    Removes any json aur wav file from mentioned directory
    """

    decision=input("This function will remove all the jsons and wav files from mentioned directory, would you like to proceed: [y/n]:\n")
    if decision.lower()=='y':
        files=list(directory_path)
        files_to_remove=[]
        for f in files:
            if 'wav' in str(f):
                files_to_remove.append(f)
            if 'json' in str(f):
                files_to_remove.append(f)
        for item in files_to_remove:
            if os.path.exists(os.path.join(os.getcwd(), item)):
                os.remove(os.path.join(os.getcwd(), item))

        print(f"These files are removed from directory {directory_path}: {files_to_remove}")
    
    elif decision.lower()=='n':
        print("Files not removed")
    else:
        print("Invalid input process aborted")


#MAIN
def transcribe(audio,speaker_audio=None, HF_TOKEN=None, tag={"message": "speech text pipeline run"}):

    """
    The main function to transcribe and diarize given audio.
    """

    domain_type="meeting"
    callSid=str(uuid.uuid4())
    output={
            "metadata": {
            "request_id": "",
            "created_at": "",
            "duration":"",
            "language":"en",
            "process_time_taken":"",
            "audio":"",
            "model_info": {"transcription_model":"medium",
                            "diarization":{"VAD": "vad_multilingual_marblenet",
                                            "speaker_embedings": "titanet_large"}}
            },
            "results": {"channels": [{"alternatives":[{"transcript": "",
                                                        "confidence": 0,
                                                        "sentences": [],
                                                        "words":[]}]}]}
    }

    if os.path.exists(os.path.join(os.getcwd(), 'dia_data')):
        shutil.rmtree(os.path.join(os.getcwd(), 'dia_data'))

    t1=time.time()

    #SUBPROCESS-1
    try:
        AUDIO_FILENAME, duration=AUDIO_DOWNLOAD(callSid, audio)

    except Exception as e:

        return_json={"status": f"No process completed for callSid: {callSid}", "return_message": f"Error in downloading audio: {e}"}
        return return_json

    #SUBPROCESS-2
    try:
        word_hyp, word_ts_hyp=STT(AUDIO_FILENAME)

    except Exception as e:

        return_json={"status": f"Process completed till audio download for callSid: {callSid}", "return_message": f"Error in transcribing: {e}"}
        return return_json

    #SUBPROCESS-3
    try:
        diarized_transcription=DIARIZATION(domain_type, AUDIO_FILENAME, word_hyp, word_ts_hyp)

    except Exception as e:

        return_json={"status": f"Process completed till transcribing for callSid: {callSid}", "return_message": f"Error in diarizing: {e}"}

        return return_json

    #SUBPROCESS-4
    if speaker_audio!=None:
        try:
            if HF_TOKEN:
                diarized_transcription=SPEAKER_MATCHING(AUDIO_FILENAME, diarized_transcription, speaker_audio, HF_TOKEN)
            else:
                diarized_transcription=SPEAKER_MATCHING(AUDIO_FILENAME, diarized_transcription, speaker_audio)
              
        except Exception as e:
          return_json={"status": f"Process completed till diarizing for callSid: {callSid}", "return_message": f"Error in Speaker matching: {e}"}
          return return_json

    speaker_names=set()
    for sentence in diarized_transcription['sentences']:
      speaker_names.add(sentence['speaker'])

    #SUBPROCESS-5
    try:

        output['metadata']['tag']=tag
        output['metadata']['request_id']+=callSid
        output['metadata']['created_at']+=str(datetime.datetime.now())
        output['metadata']['duration']+=str(duration)+' mins'
        output['metadata']['process_time_taken']+=str(round(time.time()-t1,2))+' secs'
        output['metadata']['audio']+=audio
        output['metadata']['speaker_count']=diarized_transcription['speaker_count']
        output['metadata']['speaker_names']=list(speaker_names)
        output['results']['channels'][0]['alternatives'][0]['transcript']=diarized_transcription['transcription']
        output['results']['channels'][0]['alternatives'][0]['confidence']=0.94
        output['results']['channels'][0]['alternatives'][0]['sentences']=diarized_transcription['sentences']
        output['results']['channels'][0]['alternatives'][0]['words']=diarized_transcription['words']

    except Exception as e:

        return_json={"status": f"Process completed till Speaker matching for callSid: {callSid}", "return_message": f"Error in filling data: {e}"}

        return return_json

    torch.cuda.empty_cache()
    gc.collect()

    return output