# Speech Text Pipeline

speech_text_pipeline is a Python package that allows you to process audio files for automatic speech recognition (ASR), speaker diarization, and speaker matching. It can produce transcripts with or without the identification of specific speakers based on the audio provided. The package is designed to handle both regular transcription and cases where one speaker’s identity is known and provided via an additional audio sample.

## Prerequisites

Before installing speech_text_pipeline, make sure you install the following dependencies:

- omegaconf 
- git+https://github.com/openai/whisper.git
- git+https://github.com/NVIDIA/NeMo.git

Additionally, if you want to use the speaker matching functionality, you will need access to the pyannote/embedding model hosted on Hugging Face.

1. Visit the pyannote/embedding model page on Hugging Face.

2. Create or log in to your Hugging Face account.

3. Generate your Hugging Face access token (HF_TOKEN) by going to your account settings.

4. Log in via the CLI using the following command:

`huggingface-cli login`

Then, input your `HF_TOKEN` when prompted.

Alternatively, you can pass your `HF_TOKEN` directly to the transcribe function as a parameter:

`import speech_text_pipeline as stp` 

`result = stp.transcribe(audio="path_to_audio_file.wav", speaker_audio="path_to_known_speaker_audio.wav", HF_TOKEN="Your HF_TOKEN")`

Note: The Hugging Face token is only required for the speaker matching functionality.

## Installation

Once the prerequisite packages are installed, you can install speech_text_pipeline using pip:

`pip install speech_text_pipeline`

## Usage

### Basic Transcription and Diarization (Type 1 Output)

This mode generates a transcript with speaker diarization, assigning anonymous speaker labels (e.g., "Speaker 1", "Speaker 2") to different segments of the audio.

`import speech_text_pipeline as stp`

#### Define the audio file URL or path
`audio_url = "path_to_audio_file.wav"`

#### Get transcription with speaker diarization
`result = stp.transcribe(audio=audio_url)`

#### Output type 1: Diarized transcript with anonymous speakers
`print(result)`

### Transcription with Speaker Identification (Type 2 Output)

`import speech_text_pipeline as stp`

#### Define the audio file and known speaker sample
`audio_url = "path_to_audio_file.wav"`

`agent_audio_url = "path_to_agent_audio.wav"` # Sample of the known speaker

#### Pass the Hugging Face token for speaker matching
`result = stp.transcribe(audio=audio_url, speaker_audio=agent_audio_url, HF_TOKEN="Your HF_TOKEN")`

#### Output type 2: Diarized transcript with named speaker
`print(result)`