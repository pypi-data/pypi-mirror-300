import re
import wget
import librosa
import os
import soundfile as sf

#AUDIO_DOWNLOAD
def AUDIO_DOWNLOAD(callSid, audio_URL):

    pattern=r'^https?://[^\s/$.?#].[^\s]*$'
    if re.match(pattern, audio_URL):
      path=f"{callSid}.wav"
      audio_response = wget.download(audio_URL, path)
      AUDIO_FILENAME=audio_response
    else:
      AUDIO_FILENAME=audio_URL

    signal, sample_rate = librosa.load(AUDIO_FILENAME, sr=None)
    duration=round(signal.shape[0]/(sample_rate*60), 2)

    if sample_rate>8000:
        new_sr = 8000
        audio_resampled = librosa.resample(y=signal, orig_sr=sample_rate, target_sr=new_sr)
        output_file = f"{AUDIO_FILENAME.split('/')[-1].split('.')[0]}.wav"
        sf.write(output_file, audio_resampled, new_sr)
        os.remove(AUDIO_FILENAME)
        AUDIO_FILENAME=output_file

    return AUDIO_FILENAME, duration