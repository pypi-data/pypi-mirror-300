import os
import re
import shutil
import wget
import numpy as np
import torch
import librosa
import soundfile as sf
from pyannote.audio import Model, Inference

#SIMILARITY MATCH
def SPEAKER_EMBEDDINGS_SIMILARITY(agent_audio_embeddings, audio2_embeddings):
    X=min(agent_audio_embeddings.shape[0], audio2_embeddings.shape[0])

    dot_product = np.dot(agent_audio_embeddings[:X, :].flatten(), audio2_embeddings[:X, :].flatten())
    norm_vec1 = np.linalg.norm(agent_audio_embeddings)
    norm_vec2 = np.linalg.norm(audio2_embeddings)

    sim_idx=dot_product / (norm_vec1 * norm_vec2)

    return sim_idx

#AUDIO CLIPPING
def AUDIO_CLIPPING(directory_name, speaker, duration, audio_array, sample_rate):
    start_time = duration[0]
    end_time = duration[-1]

    start_sample = librosa.time_to_samples(start_time, sr=sample_rate)
    end_sample = librosa.time_to_samples(end_time, sr=sample_rate)

    segment = audio_array[start_sample:end_sample]

    segmented_audio=os.path.join(directory_name, speaker+'.wav')
    sf.write(segmented_audio, segment, sample_rate)

#MAIN SPEAKER MATCHING FUNCTION
def SPEAKER_MATCHING(AUDIO_FILENAME, diarized_transcription, agent_audio_URL, HF_TOKEN=None):

    pattern=r'^https?://[^\s/$.?#].[^\s]*$'
    if re.match(pattern, agent_audio_URL):
        agent_audio= wget.download(agent_audio_URL, os.getcwd())
    else:
        agent_audio=os.path.join(os.getcwd(), agent_audio_URL)

    agent_name=agent_audio.split('/')[-1].split('.')[0]
    agent_speaker=""

    if HF_TOKEN:
        model = Model.from_pretrained("pyannote/embedding", HF_TOKEN=HF_TOKEN)
    else:
        model = Model.from_pretrained("pyannote/embedding")
    inference = Inference(model)
    device=torch.device("cuda" if torch.cuda.is_available() else "cpu")
    inference.to(device)

    #extracting speaker segments
    list_of_spk={}
    for sentence in diarized_transcription['sentences']:
        spk=sentence['speaker']
        s_t=float(sentence['start_time'])
        e_t=float(sentence['end_time'])
        current_spk_duration=e_t-s_t

        if spk in list(list_of_spk.keys()):
            spk_duration=list_of_spk[spk][-1]-list_of_spk[spk][0]
            if current_spk_duration>spk_duration:
                list_of_spk[spk]=[s_t, e_t]
            else:
                pass
        else:
            list_of_spk[spk]=[s_t, e_t]

    print(f"\nlist of spk: {list_of_spk}\n")

    #saving clipped audios in audio dir
    directory_name=os.path.join(os.getcwd(), 'spk_audio_clippings')
    if not os.path.exists(directory_name):
        os.mkdir(directory_name)

    audio_array, sample_rate = librosa.load(AUDIO_FILENAME, sr=None)

    for speaker in list(list_of_spk.keys()):
        AUDIO_CLIPPING(directory_name, speaker, list_of_spk[speaker], audio_array, sample_rate)

    #getting most similar speaker with agent
    agent_audio_embeddings=inference(agent_audio).data
    print(f"agent audio embeddings: {type(agent_audio_embeddings)}")
    similarity_index=-100
    for audio2 in os.listdir(directory_name):
        audio2_embeddings=inference(os.path.join(directory_name, audio2)).data

        sim_index=SPEAKER_EMBEDDINGS_SIMILARITY(agent_audio_embeddings, audio2_embeddings)
        print(f"similarity index of {agent_audio.split('/')[-1].split('.')[0]} with {audio2.split('/')[-1].split('.')[0]} is: {sim_index}")
        if sim_index>similarity_index:
            agent_speaker=audio2.split('/')[-1].split('.')[0]
            similarity_index=sim_index


    #changing speaker name with agent name
    for sentence in diarized_transcription['sentences']:
        if sentence['speaker']==agent_speaker:
            sentence['speaker']=agent_name

    for word in diarized_transcription['words']:
        if word['speaker']==agent_speaker:
            word['speaker']=agent_name

    try:
        shutil.rmtree(directory_name)
        # shutil.rmtree(agent_audio_path)
        # if os.path.exists(os.path.join(os.getcwd() ,AUDIO_FILENAME)):
        #   os.remove(os.path.join(os.getcwd() ,AUDIO_FILENAME))
    except Exception as e:
        print('Audio clippings and agent audio not removed due to error: ', e)

    return diarized_transcription